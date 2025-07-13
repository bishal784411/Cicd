import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta
import time

import requests
import uvicorn
import psutil
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse

import asyncio
# Log file paths
ERROR_LOG_PATH = Path("error_log.json")
SOLUTION_LOG_PATH = Path("solutions.json")
FIX_LOG_PATH = Path("fix_log.json")


# ---------- Agent Management ----------
class AgentLauncher:
    def __init__(self):
        self.agents = {
            'monitor': 'monitor_agent.py',
            'solution': 'solution_agent.py',
            'fix': 'fix_agent.py'
        }
        self.processes = {}

    def check_requirements(self):
        if not os.path.exists('.env') or not os.path.exists("Hotel-demo"):
            return False
        for agent_file in self.agents.values():
            if not os.path.exists(agent_file):
                return False
        return True

    def launch_agent(self, agent_name):
        if agent_name in self.processes and self.processes[agent_name].poll() is None:
            return f"{agent_name} is already running."
        try:
            process = subprocess.Popen([sys.executable, self.agents[agent_name]])
            self.processes[agent_name] = process
            return f"{agent_name} started."
        except Exception as e:
            raise RuntimeError(f"Failed to launch {agent_name}: {e}")

    def stop_agent(self, agent_name):
        if agent_name in self.processes:
            process = self.processes[agent_name]
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                return f"{agent_name} stopped."
            return f"{agent_name} is not running."
        return f"{agent_name} was never started."

    def get_status(self):
        return {
            name: "running" if proc.poll() is None else "stopped"
            for name, proc in self.processes.items()
        }


# ---------- GitHub Commit Logic ----------
def extract_error_summary():
    if not FIX_LOG_PATH.exists():
        return "Applied auto-fix (no error details available)"
    try:
        with open(FIX_LOG_PATH, "r") as f:
            data = json.load(f)
        if not data:
            return "Applied auto-fix (log empty)"
        latest_fix = data[-1]
        errors = latest_fix.get("errors", [])
        if not errors:
            return "Applied auto-fix (no errors listed)"
        cleaned_errors = [e.split("->")[0].strip() for e in errors]
        return "Fix applied: " + " | ".join(cleaned_errors)
    except Exception as e:
        return f"Applied auto-fix (error loading log: {e})"


def push_to_github():
    try:
        # Load fix_log
        with FIX_LOG_PATH.open("r", encoding="utf-8") as f:
            fix_log = json.load(f)

        # Find the latest entry that hasn't been pushed
        pending_entries = [entry for entry in reversed(fix_log) if not entry.get("isPushed")]
        if not pending_entries:
            return False, "No unpushed entries found in fix_log.json"

        latest_entry = pending_entries[0]
        commit_message = f"Fix applied to {latest_entry['file']} at {latest_entry['applied_at']}"

        # Git add, commit, push
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)

        # Mark as pushed
        for entry in fix_log:
            if entry["timestamp"] == latest_entry["timestamp"] and entry["file"] == latest_entry["file"]:
                entry["isPushed"] = True
                entry["error_push"] = None

        with open("fix_log.json", "w") as f:
            json.dump(fix_log, f, indent=2)

        print("✅ GitHub push successful")
        return True, None

    except subprocess.CalledProcessError as e:
        error_message = e.stderr if hasattr(e, 'stderr') else str(e)

        # Update entry with error
        for entry in fix_log:
            if entry["timestamp"] == latest_entry["timestamp"] and entry["file"] == latest_entry["file"]:
                entry["isPushed"] = False
                entry["error_push"] = error_message

        with open("fix_log.json", "w") as f:
            json.dump(fix_log, f, indent=2)

        print(f"❌ GitHub push failed: {error_message}")
        return False, error_message
    

# ---------- FastAPI Setup ----------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()
launcher = AgentLauncher()


@app.on_event("startup")
def startup_event():
    if not launcher.check_requirements():
        print("System requirements not met.")


# ---------- Utility Routes ----------
@api_router.get("/network/check")
def check_network():
    try:
        response = requests.head("http://www.google.com", timeout=5)
        status = response.status_code
        headers_text = "\n".join(f"{k}: {v}" for k, v in response.headers.items())
        return PlainTextResponse(f"success\nHTTP {status}\n{headers_text}")
    except requests.RequestException as e:
        return PlainTextResponse(f"failure\nNetwork check failed: {e}", status_code=503)


# ---------- Agent Control ----------
@api_router.post("/start/{agent_name}")
def start_agent(agent_name: str):
    if agent_name not in launcher.agents:
        raise HTTPException(status_code=400, detail="Unknown agent name")
    try:
        msg = launcher.launch_agent(agent_name)
        return {"message": msg}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.post("/stop/{agent_name}")
def stop_agent(agent_name: str):
    if agent_name not in launcher.agents:
        raise HTTPException(status_code=400, detail="Unknown agent name")
    return {"message": launcher.stop_agent(agent_name)}


@api_router.post("/start/all")
def start_all_agents():
    messages = [launcher.launch_agent(name) for name in launcher.agents]
    return {"message": messages}


@api_router.post("/stop/all")
def stop_all_agents():
    messages = [launcher.stop_agent(name) for name in launcher.agents]
    return {"message": messages}


@api_router.get("/status")
def get_status():
    return launcher.get_status()


# ---------- Logs: Errors ----------
@api_router.get("/errors")
def get_all_errors():
    try:
        if not ERROR_LOG_PATH.exists():
            return {"errors": []}
        return {"errors": json.load(open(ERROR_LOG_PATH))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/errors/latest")
def get_latest_error():
    try:
        data = json.load(open(ERROR_LOG_PATH)) if ERROR_LOG_PATH.exists() else []
        if not data:
            return {"error": None}
        return {"error": sorted(data, key=lambda x: x['timestamp'], reverse=True)[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/errors/detected")
def get_detected_errors():
    try:
        data = json.load(open(ERROR_LOG_PATH)) if ERROR_LOG_PATH.exists() else []
        return {"errors": [e for e in data if e.get("status") == "detected"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------- Logs: Solutions ----------
@api_router.get("/solutions")
def get_all_solutions():
    try:
        if SOLUTION_LOG_PATH.exists():
            with open(SOLUTION_LOG_PATH, "r") as f:
                raw_solutions = json.load(f)

            # Remove 'corrected_code' from each solution
            filtered_solutions = []
            for sol in raw_solutions:
                filtered = {k: v for k, v in sol.items() if k != "corrected_code"}
                filtered_solutions.append(filtered)

            return {"Solutions": filtered_solutions}
        else:
            return {"Solutions": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load Solutions log: {e}")

@api_router.get("/solution/latest")
def get_latest_solution():
    try:
        data = json.load(open(SOLUTION_LOG_PATH)) if SOLUTION_LOG_PATH.exists() else []
        if not data:
            return {"Solutions": None}

        latest = data[-1].copy()
        latest.pop("corrected_code", None)
        return {"Solutions": latest}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load latest Solutions: {e}")


@api_router.get("/solution/file/{filename}")
def get_solution_by_file(filename: str):
    try:
        data = json.load(open(SOLUTION_LOG_PATH)) if SOLUTION_LOG_PATH.exists() else []

        filtered = []
        for entry in data:
            if filename in entry.get("file", ""):
                entry_copy = entry.copy()
                entry_copy.pop("corrected_code", None)
                filtered.append(entry_copy)

        return {"Solutions": filtered}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to filter Solutions: {e}")


# ---------- Logs: Fixes ----------
@api_router.get("/fixes")
def get_all_fixes():
    try:
        return {"fixes": json.load(open(FIX_LOG_PATH)) if FIX_LOG_PATH.exists() else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load fix log: {e}")


@api_router.get("/fixes/latest")
def get_latest_fix():
    try:
        data = json.load(open(FIX_LOG_PATH)) if FIX_LOG_PATH.exists() else []
        return {"fix": data[-1] if data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load latest fix: {e}")


@api_router.get("/fixes/file/{filename}")
def get_fixes_by_file(filename: str):
    try:
        data = json.load(open(FIX_LOG_PATH)) if FIX_LOG_PATH.exists() else []
        return {"fixes": [f for f in data if filename in f.get("file", "")]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to filter fixes: {e}")


# ---------- Dashboard Stats ----------
def count_entries_by_date(log, today, week_ago):
    today_count = 0
    week_count = 0
    for entry in log:
        try:
            ts = datetime.strptime(entry.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
            if ts.date() == today.date():
                today_count += 1
            if ts >= week_ago:
                week_count += 1
        except Exception:
            continue
    return today_count, week_count


@api_router.get("/dashboard/stats")
def get_dashboard_stats():
    today = datetime.now()
    week_ago = today - timedelta(days=7)

    try:
        errors = json.load(open(ERROR_LOG_PATH)) if ERROR_LOG_PATH.exists() else []
        solutions = json.load(open(SOLUTION_LOG_PATH)) if SOLUTION_LOG_PATH.exists() else []
        fixes = json.load(open(FIX_LOG_PATH)) if FIX_LOG_PATH.exists() else []

        error_today, error_week = count_entries_by_date(errors, today, week_ago)
        solution_today, solution_week = count_entries_by_date(solutions, today, week_ago)
        fix_today, fix_week = count_entries_by_date(fixes, today, week_ago)

        return {
            "monitored": {"today": error_today, "week": error_week},
            "solutions": {"today": solution_today, "week": solution_week},
            "fixes": {"today": fix_today, "week": fix_week}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get dashboard stats: {e}")


# ---------- GitHub Push ----------
@api_router.post("/github/push")
def push_code_to_github():
    success, error = push_to_github()
    if success:
        return {"message": "GitHub push successful."}
    else:
        raise HTTPException(status_code=500, detail=f"GitHub push failed: {error}")


# ---------- Agent process info helper ----------
def get_agent_process_info(process: subprocess.Popen):
    try:
        p = psutil.Process(process.pid)
        uptime_sec = time.time() - p.create_time()
        uptime_str = str(timedelta(seconds=int(uptime_sec)))
        cpu_percent = p.cpu_percent(interval=0.1)
        mem_info = p.memory_info()
        mem_mb = mem_info.rss / 1024 / 1024  # Resident Set Size in MB
        return {
            "pid": p.pid,
            "uptime": uptime_str,
            "cpu_percent": cpu_percent,
            "memory_mb": round(mem_mb, 2),
            "status": "running" if p.is_running() else "stopped",
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return {
            "pid": None,
            "uptime": None,
            "cpu_percent": None,
            "memory_mb": None,
            "status": "stopped",
        }


# ---------- Health Status (live stats for agents) ----------
@api_router.get("/health/status")
def system_health():
    try:
        agents_info = {}
        for name, process in launcher.processes.items():
            if process.poll() is None:
                agents_info[name] = get_agent_process_info(process)
            else:
                agents_info[name] = {
                    "pid": None,
                    "uptime": None,
                    "cpu_percent": None,
                    "memory_mb": None,
                    "status": "stopped",
                }

        return {
            "status": "healthy",
            "agents": agents_info,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {e}")


@api_router.get("/health/status/{agent_name}/stream")
@api_router.get("/health/status/{agent_name}/stream")
async def stream_agent_health(agent_name: str):
    agent_name = agent_name.lower()
    if agent_name not in launcher.agents:
        raise HTTPException(status_code=404, detail="Unknown agent name")

    process = launcher.processes.get(agent_name)
    if not process or process.poll() is not None:
        async def stopped_event_generator():
            while True:
                data = {
                    "agent": agent_name,
                    "status": "stopped",
                    "uptime": None,
                    "cpu_percent": None,
                    "memory_mb": None,
                }
                yield f"data: {json.dumps(data)}\n\n"
                await asyncio.sleep(3)
        return StreamingResponse(stopped_event_generator(), media_type="text/event-stream")

    # Warm-up once
    try:
        p = psutil.Process(process.pid)
        p.cpu_percent(interval=None)
    except Exception:
        pass

    async def event_generator():
        while True:
            try:
                p = psutil.Process(process.pid)

                now = time.time()
                uptime_sec = now - p.create_time()
                uptime_str = str(timedelta(seconds=int(uptime_sec)))

                cpu_percent = p.cpu_percent(interval=1.0)
                mem_mb = p.memory_info().rss / 1024 / 1024

                data = {
                    "agent": agent_name,
                    "status": "running",
                    "uptime": uptime_str,
                    "cpu_percent": round(cpu_percent, 2),
                    "memory_mb": round(mem_mb, 2),
                }
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                data = {
                    "agent": agent_name,
                    "status": "stopped",
                    "uptime": None,
                    "cpu_percent": None,
                    "memory_mb": None,
                    "error": str(e),
                }
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(2)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
# ---------- Include Router ----------
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("launcher:app", host="0.0.0.0", port=5000, reload=True)
