import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta
import time, shlex
import threading
import requests, re
import uvicorn
import psutil
from fastapi import FastAPI, HTTPException, APIRouter, BackgroundTasks, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse, JSONResponse
from solution_agent import SolutionAgent
from monitor_agent import MonitorAgent
from fix_agent import AIFixAgent
from typing import Optional
import asyncio
# Log file paths
ERROR_LOG_PATH = Path("error_log.json")
SOLUTION_LOG_PATH = Path("solutions.json")
FIX_LOG_PATH = Path("fix_log.json")
flOW_LOG_PATH = Path("process_flow.json")
commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()


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
            process = subprocess.Popen(
                [sys.executable, "-u", self.agents[agent_name]],  # <- Add "-u" here
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )

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
    
def push_to_github_stream():
    try:
        with FIX_LOG_PATH.open("r", encoding="utf-8") as f:
            fix_log = json.load(f)

        pending_entries = [entry for entry in reversed(fix_log) if not entry.get("isPushed")]
        if not pending_entries:
            yield "⚠️ No unpushed entries found in fix_log.json"
            return

        latest_entry = pending_entries[0]
        err_id = latest_entry.get("err_id")
        file = latest_entry.get("file")
        fix_id = latest_entry.get("fix_id")

        commit_message = f"Fix applied to {file} at {latest_entry['applied_at']}"
        yield f"🔧 Preparing to commit: {commit_message}"

        subprocess.run(["git", "add", "."], check=True)
        yield "📦 Added files."

        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        yield "✍️ Committed changes."

        subprocess.run(["git", "push", "-u", "origin", "master"], check=True)
        yield "🚀 Pushed to GitHub."

        # ✅ Update fix_log.json as pushed
        for entry in fix_log:
            if entry.get("err_id") == err_id and entry.get("file") == file:
                entry["isPushed"] = True
                entry["error_push"] = None

        with FIX_LOG_PATH.open("w") as f:
            json.dump(fix_log, f, indent=2)
        yield "💾 fix_log.json marked as pushed."

        # ✅ Get latest Git metadata
        commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()

        # ✅ Helper to update individual log files
        def update_commit_info_in_file(filepath):
            if not os.path.exists(filepath):
                return
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            updated = False
            for item in data:
                if item.get("err_id") == err_id and item.get("file") == file:
                    item["commit_hash"] = commit_hash
                    item["git_push"] = "pushed"
                    item["branch"] = branch
                    updated = True

            if updated:
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)

        for path in ["error_log.json", "solutions.json", "fix_log.json"]:
            update_commit_info_in_file(path)
            yield f"🔄 Updated {path} with commit metadata."

        # ✅ Update process_flow.json -> Deploy block
        if flOW_LOG_PATH.exists():
            with flOW_LOG_PATH.open("r", encoding="utf-8") as f:
                flow_data = json.load(f)

            existing_ids = []

            for item in flow_data:
                dep_id = item.get("Deploy", {}).get("Dep_id", "Dep-000")
                if dep_id and "-" in dep_id:
                    try:
                        existing_ids.append(int(dep_id.split("-")[1]))
                    except (IndexError, ValueError):
                        continue

            next_dep_id = f"Dep-{max(existing_ids, default=0) + 1:03}"

            for item in flow_data:
                if item.get("filename") == file and item.get("Fix", {}).get("fix_id") == fix_id:
                    item["Deploy"] = {
                        "Dep_id": next_dep_id,
                        "status": "deployed",
                        "time": datetime.now().strftime("%I:%M:%S %p"),
                        "analysis": commit_hash
                    }

            with flOW_LOG_PATH.open("w") as f:
                json.dump(flow_data, f, indent=2)
            yield "📦 process_flow.json updated with deployment info."

        yield "✅ All logs updated successfully."

    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if hasattr(e, 'stderr') and e.stderr else str(e)
        yield f"❌ GitHub push failed: {error_msg}"

        for entry in fix_log:
            if entry.get("err_id") == err_id and entry.get("file") == file:
                entry["isPushed"] = False
                entry["error_push"] = error_msg

        with FIX_LOG_PATH.open("w") as f: 
            json.dump(fix_log, f, indent=2)
        yield "💾 fix_log.json updated with push error."


# def push_to_github_stream():
#     try:
#         with FIX_LOG_PATH.open("r", encoding="utf-8") as f:
#             fix_log = json.load(f)

#         pending_entries = [entry for entry in reversed(fix_log) if not entry.get("isPushed")]
#         if not pending_entries:
#             yield "⚠️ No unpushed entries found in fix_log.json"
#             return

#         latest_entry = pending_entries[0]
#         err_id = latest_entry.get("err_id")
#         file = latest_entry.get("file")
#         fix_id = latest_entry.get("fix_id")

#         commit_message = f"Fix applied to {file} at {latest_entry['applied_at']}"
#         yield f"🔧 Preparing to commit: {commit_message}"

#         # Check git status first
#         try:
#             result = subprocess.run(["git", "status", "--porcelain"], 
#                                   capture_output=True, text=True, check=True)
#             if not result.stdout.strip():
#                 yield "ℹ️ No changes to commit. Repository is already up to date."
#                 # Still mark as pushed since there's nothing to push
#                 for entry in fix_log:
#                     if entry.get("err_id") == err_id and entry.get("file") == file:
#                         entry["isPushed"] = True
#                         entry["error_push"] = None
                
#                 with FIX_LOG_PATH.open("w") as f:
#                     json.dump(fix_log, f, indent=2)
#                 yield "✅ Entry marked as pushed (no changes needed)"
#                 return
#             else:
#                 yield f"📋 Changes detected: {len(result.stdout.strip().split(chr(10)))} files modified"
#         except subprocess.CalledProcessError as e:
#             yield f"⚠️ Git status check failed: {e}"

#         # Add files
#         try:
#             subprocess.run(["git", "add", "."], check=True, capture_output=True)
#             yield "📦 Added files."
#         except subprocess.CalledProcessError as e:
#             yield f"❌ Git add failed: {e}"
#             raise

#         # Check if we have git user configured
#         try:
#             subprocess.run(["git", "config", "user.name"], check=True, capture_output=True)
#             subprocess.run(["git", "config", "user.email"], check=True, capture_output=True)
#         except subprocess.CalledProcessError:
#             yield "⚙️ Configuring git user..."
#             try:
#                 subprocess.run(["git", "config", "user.name", "AutoFix Bot"], check=True)
#                 subprocess.run(["git", "config", "user.email", "autofix@example.com"], check=True)
#                 yield "✅ Git user configured"
#             except subprocess.CalledProcessError as e:
#                 yield f"❌ Failed to configure git user: {e}"

#         # Commit changes
#         try:
#             result = subprocess.run(["git", "commit", "-m", commit_message], 
#                                   check=True, capture_output=True, text=True)
#             yield "✍️ Committed changes."
#             if result.stdout:
#                 yield f"📝 {result.stdout.strip()}"
#         except subprocess.CalledProcessError as e:
#             if e.returncode == 1:
#                 # Check if it's because there's nothing to commit
#                 if "nothing to commit" in (e.stdout or "") or "nothing to commit" in (e.stderr or ""):
#                     yield "ℹ️ Nothing to commit, working tree clean."
#                     # Mark as pushed since there's nothing to push
#                     for entry in fix_log:
#                         if entry.get("err_id") == err_id and entry.get("file") == file:
#                             entry["isPushed"] = True
#                             entry["error_push"] = None
                    
#                     with FIX_LOG_PATH.open("w") as f:
#                         json.dump(fix_log, f, indent=2)
#                     yield "✅ Entry marked as pushed (nothing to commit)"
#                     return
#                 else:
#                     yield f"❌ Commit failed: {e.stderr or e.stdout or str(e)}"
#                     raise
#             else:
#                 yield f"❌ Commit failed with exit code {e.returncode}: {e.stderr or e.stdout or str(e)}"
#                 raise

#         # Push to GitHub
#         try:
#             result = subprocess.run(["git", "push"], check=True, capture_output=True, text=True)
#             yield "🚀 Pushed to GitHub."
#             if result.stdout:
#                 yield f"📤 {result.stdout.strip()}"
#         except subprocess.CalledProcessError as e:
#             yield f"❌ Push failed: {e.stderr or e.stdout or str(e)}"
#             raise

#         # ✅ Update fix_log.json as pushed
#         for entry in fix_log:
#             if entry.get("err_id") == err_id and entry.get("file") == file:
#                 entry["isPushed"] = True
#                 entry["error_push"] = None

#         with FIX_LOG_PATH.open("w") as f:
#             json.dump(fix_log, f, indent=2)
#         yield "💾 fix_log.json marked as pushed."

#         # ✅ Get latest Git metadata
#         try:
#             commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
#             branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
#             yield f"🔗 Commit hash: {commit_hash[:8]}"
#             yield f"🌿 Branch: {branch}"
#         except subprocess.CalledProcessError as e:
#             yield f"⚠️ Could not get git metadata: {e}"
#             commit_hash = "unknown"
#             branch = "unknown"

#         # ✅ Helper to update individual log files
#         def update_commit_info_in_file(filepath):
#             if not os.path.exists(filepath):
#                 return False
#             try:
#                 with open(filepath, "r", encoding="utf-8") as f:
#                     data = json.load(f)

#                 updated = False
#                 for item in data:
#                     if item.get("err_id") == err_id and item.get("file") == file:
#                         item["commit_hash"] = commit_hash
#                         item["git_push"] = "pushed"
#                         item["branch"] = branch
#                         updated = True

#                 if updated:
#                     with open(filepath, "w", encoding="utf-8") as f:
#                         json.dump(data, f, indent=2)
#                 return updated
#             except Exception as e:
#                 yield f"⚠️ Error updating {filepath}: {e}"
#                 return False

#         for path in ["error_log.json", "solutions.json", "fix_log.json"]:
#             if update_commit_info_in_file(path):
#                 yield f"🔄 Updated {path} with commit metadata."
#             else:
#                 yield f"⚠️ Could not update {path}"

#         # ✅ Update process_flow.json -> Deploy block
#         try:
#             if flOW_LOG_PATH.exists():
#                 with flOW_LOG_PATH.open("r", encoding="utf-8") as f:
#                     flow_data = json.load(f)

#                 existing_ids = []

#                 for item in flow_data:
#                     dep_id = item.get("Deploy", {}).get("Dep_id", "Dep-000")
#                     if dep_id and "-" in dep_id:
#                         try:
#                             existing_ids.append(int(dep_id.split("-")[1]))
#                         except (IndexError, ValueError):
#                             continue

#                 next_dep_id = f"Dep-{max(existing_ids, default=0) + 1:03}"

#                 for item in flow_data:
#                     if item.get("filename") == file and item.get("Fix", {}).get("fix_id") == fix_id:
#                         item["Deploy"] = {
#                             "Dep_id": next_dep_id,
#                             "status": "deployed",
#                             "time": datetime.now().strftime("%I:%M:%S %p"),
#                             "analysis": commit_hash
#                         }

#                 with flOW_LOG_PATH.open("w") as f:
#                     json.dump(flow_data, f, indent=2)
#                 yield "📦 process_flow.json updated with deployment info."
#             else:
#                 yield "⚠️ process_flow.json not found"
#         except Exception as e:
#             yield f"⚠️ Error updating process_flow.json: {e}"

#         yield "✅ All logs updated successfully."

#     except subprocess.CalledProcessError as e:
#         error_msg = f"Command failed with exit code {e.returncode}"
#         if e.stderr:
#             error_msg += f": {e.stderr.decode() if isinstance(e.stderr, bytes) else e.stderr}"
#         elif e.stdout:
#             error_msg += f": {e.stdout.decode() if isinstance(e.stdout, bytes) else e.stdout}"
        
#         yield f"❌ GitHub push failed: {error_msg}"

#         # Update fix_log with error
#         try:
#             for entry in fix_log:
#                 if entry.get("err_id") == err_id and entry.get("file") == file:
#                     entry["isPushed"] = False
#                     entry["error_push"] = error_msg

#             with FIX_LOG_PATH.open("w") as f: 
#                 json.dump(fix_log, f, indent=2)
#             yield "💾 fix_log.json updated with push error."
#         except Exception as update_error:
#             yield f"❌ Could not update fix_log.json: {update_error}"

#     except Exception as e:
#         yield f"❌ Unexpected error: {str(e)}"

# ---------- FastAPI Setup ----------
app = FastAPI()



# You can add additional URLs to this list, for example, the frontend's production domain, or other frontends.
allowed_origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["X-Requested-With", "Content-Type"],
)


agent_map = {
    "solution": SolutionAgent(),
    "monitor": MonitorAgent(),
    "fix": AIFixAgent()
}

api_router = APIRouter()
launcher = AgentLauncher()


@app.on_event("startup")
def startup_event():
    if not launcher.check_requirements():
        print("System requirements not met.")


@api_router.get("/github/push/stream")
def stream_push_to_github():
    def event_generator():
        for log_line in push_to_github():
            yield f"data: {log_line}\n\n"
    return StreamingResponse(event_generator(), media_type="text/event-stream")


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


@api_router.get("/solution/resolve/{err_id}")
def resolve_specific_error(err_id: str):
    try:
        script_dir = os.path.abspath(os.path.dirname("solution_agent.py"))
        process = subprocess.Popen(
            [sys.executable, "solution_agent.py", "--err-id", err_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=script_dir,
        )
        return {"message": f"🔄 SolutionAgent started for error ID: {err_id}", "pid": process.pid}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@api_router.get("/solution/{err_id}/stream/logs")
async def stream_solution_logs(err_id: str):
    # Launch the subprocess with unbuffered output
    process = subprocess.Popen(
        [sys.executable, "-u", "solution_agent.py", "--err-id", err_id],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    queue = asyncio.Queue()
    loop = asyncio.get_running_loop()

    def enqueue_output(stream, prefix):
        for line in iter(stream.readline, ''):
            if not line:
                break
            asyncio.run_coroutine_threadsafe(queue.put(f"{prefix} {line.strip()}"), loop)
        stream.close()

    # Start threads to read stdout and stderr
    threading.Thread(target=enqueue_output, args=(process.stdout, "OUT:"), daemon=True).start()
    threading.Thread(target=enqueue_output, args=(process.stderr, "ERR:"), daemon=True).start()

    async def event_generator():
        while True:
            try:
                line = await queue.get()
                yield f"data: {line}\n\n"
            except asyncio.CancelledError:
                # If client disconnects, terminate the process
                if process.poll() is None:
                    process.terminate()
                break

            # Exit if process finished and queue empty
            if process.poll() is not None and queue.empty():
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")
    
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

@api_router.get("/agent/{agent_name}/logs/stream")
async def stream_agent_logs(agent_name: str):
    agent_name = agent_name.lower()
    if agent_name not in launcher.agents:
        raise HTTPException(status_code=404, detail="Unknown agent")

    process = launcher.processes.get(agent_name)
    if not process or process.poll() is not None:
        async def stopped_gen():
            while True:
                yield f"data: Agent '{agent_name}' not running.\n\n"
                await asyncio.sleep(3)
        return StreamingResponse(stopped_gen(), media_type="text/event-stream")

    queue = asyncio.Queue()

    loop = asyncio.get_running_loop()

    def read_stream(stream, prefix, loop):
        for line in iter(stream.readline, ''):
            if not line:
                break
            asyncio.run_coroutine_threadsafe(queue.put(f"{prefix} {line.strip()}"), loop)
        stream.close()

    threading.Thread(target=read_stream, args=(process.stdout, "OUT:", loop), daemon=True).start()
    threading.Thread(target=read_stream, args=(process.stderr, "ERR:", loop), daemon=True).start()

    async def event_generator():
        while True:
            line = await queue.get()
            yield f"data: {line}\n\n"
            if process.poll() is not None and queue.empty():
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@api_router.get("/agents/process/flow")
def get_all_deployments(
    err_id: Optional[str] = Query(None),
    filename: Optional[str] = Query(None),
    dep_id: Optional[str] = Query(None)
):
    if not flOW_LOG_PATH.exists():
        return JSONResponse(content={"error": "process_flow.json not found"}, status_code=404)

    with flOW_LOG_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    # Optional filters
    filtered = []
    for entry in data:
        if err_id and entry.get("monitor", {}).get("error_id") != err_id:
            continue
        if filename and entry.get("filename") != filename:
            continue
        if dep_id and entry.get("Deploy", {}).get("Dep_id") != dep_id:
            continue
        filtered.append(entry)

    return filtered



@api_router.get("/system/usages")
async def live_system_stats():
    async def event_generator():
        while True:
            cpu = psutil.cpu_percent(interval=None)  # non-blocking
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            timestamp = datetime.now().isoformat()
            data = {
                "timestamp": timestamp,
                "cpu_percent": cpu,
                "memory_percent": memory,
                "disk_percent": disk
            }
            yield f"data: {data}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


from fastapi.responses import StreamingResponse
from fastapi import Request
import subprocess, re, socket, asyncio, json

@api_router.get("/network/status", response_class=StreamingResponse)
def stream_network_status(request: Request):
    def get_ssid_linux():
        try:
            result = subprocess.check_output(["iwgetid", "-r"], text=True).strip()
            return result if result else "Unknown"
        except subprocess.CalledProcessError:
            return "Unknown"

    def get_latency(host="8.8.8.8"):
        try:
            output = subprocess.check_output(["ping", "-c", "1", host], stderr=subprocess.STDOUT, text=True)
            match = re.search(r'time=(\d+\.\d+)', output)
            if match:
                return float(match.group(1))
        except subprocess.CalledProcessError:
            return None

    def is_reachable(host, port=443, timeout=2):  # Default to HTTPS
        try:
            socket.setdefaulttimeout(timeout)
            with socket.create_connection((host, port)):
                return True
        except Exception:
            return False

    async def event_generator():
        while True:
            ssid = get_ssid_linux()
            latency = get_latency()

            backend_host = request.client.host or "127.0.0.1"
            backend_port = 5000
            backend_reachable = is_reachable(backend_host, backend_port)

            google_reachable = is_reachable("www.google.com", 443)
            github_reachable = is_reachable("github.com", 443)
            npm_reachable = is_reachable("registry.npmjs.org", 443)

            data = {
                "wifi_ssid": ssid,
                "wifi_latency_ms": latency,
                "backend": {
                    "host": backend_host,
                    "port": backend_port,
                    "reachable": backend_reachable
                },
                "external_services": {
                    "google.com": google_reachable,
                    "github.com": github_reachable,
                    "npm_registry": npm_reachable
                }
            }

            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(3)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

agent_heartbeat = {}



@api_router.get("/agents/list")
def list_agents():
    now = datetime.now()

    # Load logs
    def load_json(path):
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return []

    error_log = load_json(ERROR_LOG_PATH)
    solution_log = load_json(SOLUTION_LOG_PATH)
    fix_log = load_json(FIX_LOG_PATH)

    # total_detections = len(error_log)
    monitor_detections = len(error_log)
    solution_detections = len(solution_log)
    fix_detections = len(fix_log)

    # Solution stats
    solutions_provided = len([s for s in solution_log if s.get("status") in ["Analyzed", "Provided"]])
    solutions_pending = solution_detections - solutions_provided

    # Fix stats
    fixes_applied = len([f for f in fix_log if f.get("status") == "applied"])
    fixes_pending = fix_detections - fixes_applied

    def agent_info(name):
        proc = launcher.processes.get(name)
        info = {
            "status": "stopped",
            "last_heartbeat": agent_heartbeat.get(name),
            "uptime": None,
            "total_detections": monitor_detections
        }

        if proc and proc.poll() is None:
            try:
                p = psutil.Process(proc.pid)
                uptime = now - datetime.fromtimestamp(p.create_time())
                info["status"] = "running"
                info["last_heartbeat"] = now.isoformat()
                info["uptime"] = str(uptime).split(".")[0]
                agent_heartbeat[name] = info["last_heartbeat"]
            except Exception:
                pass

        return info

    response = {
        "agents": {
            "monitor": agent_info("monitor"),
            "solution": {
                **agent_info("solution"),
                 "total_detections": solution_detections,
                "solutions_provided": solutions_provided,
                "solutions_pending": solutions_pending
            },
            "fix": {
                **agent_info("fix"),
                "total_detections": fix_detections,
                "fixes_applied": fixes_applied,
                "fixes_pending": fixes_pending
            }
        }
    }

    return JSONResponse(content=response)

# ---------- Include Router ----------
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("launcher:app", host="0.0.0.0", port=5000, reload=True)
