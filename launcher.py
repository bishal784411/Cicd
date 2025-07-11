# import os
# import json
# from pathlib import Path
# from fastapi import FastAPI, HTTPException, APIRouter
# from fastapi.middleware.cors import CORSMiddleware
# import subprocess
# import sys
# import uvicorn
# import requests
# from datetime import datetime, timedelta
# from fastapi.responses import PlainTextResponse

# ERROR_LOG_PATH = Path("error_log.json")

# Solution_LOG_PATH = Path("solutions.json")
# FIX_LOG_PATH = Path("fix_log.json")

# class AgentLauncher:
#     def __init__(self):
#         self.agents = {
#             'monitor': 'monitor_agent.py',
#             'solution': 'solution_agent.py',
#             'fix': 'fix_agent.py'
#         }
#         self.processes = {}

#     def check_requirements(self):
#         if not os.path.exists('.env') or not os.path.exists('Hotel-demo'):
#             return False
#         for agent_file in self.agents.values():
#             if not os.path.exists(agent_file):
#                 return False
#         return True

#     def launch_agent(self, agent_name):
#         agent_file = self.agents[agent_name]
#         if agent_name in self.processes and self.processes[agent_name].poll() is None:
#             return f"{agent_name} is already running."

#         try:
#             process = subprocess.Popen([sys.executable, agent_file])
#             self.processes[agent_name] = process
#             return f"{agent_name} started."
#         except Exception as e:
#             raise RuntimeError(f"Failed to launch {agent_name}: {e}")

#     def stop_agent(self, agent_name):
#         if agent_name in self.processes:
#             process = self.processes[agent_name]
#             if process.poll() is None:
#                 process.terminate()
#                 try:
#                     process.wait(timeout=5)
#                 except subprocess.TimeoutExpired:
#                     process.kill()
#                 return f"{agent_name} stopped."
#             return f"{agent_name} is not running."
#         return f"{agent_name} was never started."

#     def get_status(self):
#         status = {}
#         for name, proc in self.processes.items():
#             running = proc.poll() is None
#             status[name] = "running" if running else "stopped"
#         return status
    
    

# def extract_error_summary():
#     if not FIX_LOG_PATH.exists():
#         return "🔧 Applied auto-fix (no error details available)"

#     try:
#         with open(FIX_LOG_PATH, "r") as f:
#             data = json.load(f)

#         if not data:
#             return "🔧 Applied auto-fix (log empty)"

#         latest_fix = data[-1]
#         errors = latest_fix.get("errors", [])
#         if not errors:
#             return "🔧 Applied auto-fix (no errors listed)"

#         # Extract part before '->' from each error
#         cleaned_errors = [e.split("->")[0].strip() for e in errors]
#         error_summary = " | ".join(cleaned_errors)

#         return f"🛠️ Fix applied: {error_summary}"

#     except Exception as e:
#         return f"🔧 Applied auto-fix (error loading log: {e})"
    
# def push_to_github():
#     commit_msg = extract_error_summary()
#     try:
#         subprocess.run(["git", "add", "."], check=True)

#         commit_result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)

#         if "nothing to commit" in commit_result.stdout.lower():
#             print("⚠️ No changes to commit.")
#             return False

#         push_result = subprocess.run(["git", "push"], capture_output=True, text=True)

#         if push_result.returncode == 0:
#             print("✅ Code pushed to GitHub successfully.")
#             return True
#         else:
#             print("❌ Push failed:")
#             print(push_result.stderr)
#             return False

#     except subprocess.CalledProcessError as e:
#         print("❌ Git command failed:")
#         print(e.stderr if hasattr(e, 'stderr') else str(e))
#         return False
    
    
# # --- FastAPI app setup ---
# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # restrict in production!
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# api_router = APIRouter()
# launcher = AgentLauncher()


# @app.on_event("startup")
# def startup_event():
#     if not launcher.check_requirements():
#         print("System requirements not met. Fix .env, Hotel-demo, or missing agents.")


# @api_router.get("/network/check")
# def check_network():
#     try:
#         response = requests.head("http://www.google.com", timeout=5)
#         status = response.status_code
#         headers = response.headers
#         headers_text = "\n".join(f"{k}: {v}" for k, v in headers.items())
#         return PlainTextResponse(
#             f"success\nHTTP/{response.raw.version // 10}.{response.raw.version % 10} {status} {response.reason}\n{headers_text}"
#         )
#     except requests.RequestException as e:
#         return PlainTextResponse(f"failure\nNetwork check failed: {e}", status_code=503)
    
# @api_router.post("/start/{agent_name}")
# def start_agent(agent_name: str):
#     if agent_name not in launcher.agents:
#         raise HTTPException(status_code=400, detail="Unknown agent name")
#     try:
#         msg = launcher.launch_agent(agent_name)
#         return {"message": msg}
#     except RuntimeError as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @api_router.post("/stop/{agent_name}")
# def stop_agent(agent_name: str):
#     if agent_name not in launcher.agents:
#         raise HTTPException(status_code=400, detail="Unknown agent name")
#     msg = launcher.stop_agent(agent_name)
#     return {"message": msg}

# @api_router.get("/status")
# def status():
#     return launcher.get_status()

# @api_router.post("/start/all")
# def start_all():
#     messages = []
#     for agent_name in launcher.agents:
#         try:
#             messages.append(launcher.launch_agent(agent_name))
#         except RuntimeError as e:
#             messages.append(str(e))
#     return {"message": messages}

# @api_router.post("/stop/all")
# def stop_all():
#     messages = []
#     for agent_name in launcher.agents:
#         messages.append(launcher.stop_agent(agent_name))
#     return {"message": messages}

# @api_router.get("/errors")
# def get_all_errors():
#     if not ERROR_LOG_PATH.exists():
#         return {"errors": []}
#     try:
#         with open(ERROR_LOG_PATH, 'r') as f:
#             data = json.load(f)
#         return {"errors": data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @api_router.get("/errors/latest")
# def get_latest_error():
#     if not ERROR_LOG_PATH.exists():
#         return {"error": None}
#     try:
#         with open(ERROR_LOG_PATH, 'r') as f:
#             data = json.load(f)
#             if not data:
#                 return {"error": None}
#             latest = sorted(data, key=lambda e: e['timestamp'], reverse=True)[0]
#             return {"error": latest}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @api_router.get("/errors/detected")
# def get_detected_errors():
#     if not ERROR_LOG_PATH.exists():
#         return {"errors": []}
#     try:
#         with open(ERROR_LOG_PATH, 'r') as f:
#             data = json.load(f)
#             detected = [e for e in data if e.get('status') == 'detected']
#             return {"errors": detected}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # This is for solution agent



# @api_router.get("/solutions")
# def get_all_Solutions():
#     if not Solution_LOG_PATH.exists():
#         return {"Solutions": []}
#     try:
#         with open(Solution_LOG_PATH, "r") as f:
#             data = json.load(f)
#         return {"Solutions": data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to load Solutions log: {e}")

# @api_router.get("/solution/latest")
# def get_latest_Solutions():
#     if not Solution_LOG_PATH.exists():
#         return {"Solutions": None}
#     try:
#         with open(Solution_LOG_PATH, "r") as f:
#             data = json.load(f)
#             if not data:
#                 return {"Solutions": None}
#             latest = data[-1]
#             return {"Solutions": latest}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to load latest Solutions: {e}")

# @api_router.get("/solution/file/{filename}")
# def get_Solutions_by_file(filename: str):
#     if not Solution_LOG_PATH.exists():
#         return {"Solutions": []}
#     try:
#         with open(Solution_LOG_PATH, "r") as f:
#             data = json.load(f)
#             filtered = [f for f in data if filename in f.get("file", "")]
#             return {"Solutions": filtered}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to filter Solutions: {e}")

# # this is for fix agent

# @api_router.get("/fixes")
# def get_all_fixes():
#     if not FIX_LOG_PATH.exists():
#         return {"fixes": []}
#     try:
#         with open(FIX_LOG_PATH, "r") as f:
#             data = json.load(f)
#         return {"fixes": data}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to load fix log: {e}")

# @api_router.get("/fixes/latest")
# def get_latest_fix():
#     if not FIX_LOG_PATH.exists():
#         return {"fix": None}
#     try:
#         with open(FIX_LOG_PATH, "r") as f:
#             data = json.load(f)
#             if not data:
#                 return {"fix": None}
#             latest = data[-1]
#             return {"fix": latest}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to load latest fix: {e}")

# @api_router.get("/fixes/file/{filename}")
# def get_fixes_by_file(filename: str):
#     if not FIX_LOG_PATH.exists():
#         return {"fixes": []}
#     try:
#         with open(FIX_LOG_PATH, "r") as f:
#             data = json.load(f)
#             filtered = [f for f in data if filename in f.get("file", "")]
#             return {"fixes": filtered}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to filter fixes: {e}")


# def count_entries_by_date(log, today, week_ago):
#     today_count = 0
#     week_count = 0
#     for entry in log:
#         try:
#             timestamp = datetime.strptime(entry.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
#             if timestamp.date() == today.date():
#                 today_count += 1
#             if timestamp >= week_ago:
#                 week_count += 1
#         except Exception:
#             continue
#     return today_count, week_count

# @api_router.get("/dashboard/stats")
# def get_dashboard_stats():
#     today = datetime.now()
#     week_ago = today - timedelta(days=7)

#     try:
#         # Load logs
#         fixes = json.load(open(FIX_LOG_PATH)) if FIX_LOG_PATH.exists() else []
#         solutions = json.load(open(Solution_LOG_PATH)) if Solution_LOG_PATH.exists() else []
#         errors = json.load(open(ERROR_LOG_PATH)) if ERROR_LOG_PATH.exists() else []

#         fix_today, fix_week = count_entries_by_date(fixes, today, week_ago)
#         solution_today, solution_week = count_entries_by_date(solutions, today, week_ago)
#         error_today, error_week = count_entries_by_date(errors, today, week_ago)

#         return {
#             "monitored": {"today": error_today, "week": error_week},
#             "solutions": {"today": solution_today, "week": solution_week},
#             "fixes": {"today": fix_today, "week": fix_week}
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Failed to get dashboard stats: {e}")

# @api_router.post("/github/push")
# def push_code_to_github():
#     success = push_to_github()
#     if success:
#         return {"message": "✅ GitHub push successful."}
#     else:
#         raise HTTPException(status_code=500, detail="❌ GitHub push failed. See server logs for details.")


# app.include_router(api_router, prefix="/api")

# if __name__ == "__main__":
#     uvicorn.run("launcher:app", host="0.0.0.0", port=5000, reload=True)


import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta

import requests
import uvicorn
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

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
        if not os.path.exists('.env') or not os.path.exists('Hotel-demo'):
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


# def push_to_github():
#     commit_msg = extract_error_summary()
#     try:
#         subprocess.run(["git", "add", "."], check=True)
#         commit_result = subprocess.run(["git", "commit", "-m", commit_msg], capture_output=True, text=True)
#         if "nothing to commit" in commit_result.stdout.lower():
#             print("No changes to commit.")
#             return False
#         push_result = subprocess.run(["git", "push"], capture_output=True, text=True)
#         if push_result.returncode == 0:
#             print("Code pushed to GitHub successfully.")
#             return True
#         else:
#             print("Push failed:", push_result.stderr)
#             return False
#     except subprocess.CalledProcessError as e:
#         print("Git command failed:", e.stderr if hasattr(e, 'stderr') else str(e))
#         return False


def push_to_github():
    commit_msg = extract_error_summary()
    try:
        print("🔍 Adding files...")
        subprocess.run(["git", "add", "."], check=True)

        print("📝 Committing...")
        commit_result = subprocess.run(
            ["git", "commit", "-m", commit_msg], capture_output=True, text=True
        )
        print("Commit stdout:", commit_result.stdout)
        print("Commit stderr:", commit_result.stderr)

        if "nothing to commit" in commit_result.stdout.lower():
            print("No changes to commit.")
            return False

        print("📤 Pushing to GitHub...")
        push_result = subprocess.run(
            ["git", "push"], capture_output=True, text=True
        )
        print("Push stdout:", push_result.stdout)
        print("Push stderr:", push_result.stderr)

        if push_result.returncode == 0:
            print("Code pushed to GitHub successfully.")
            return True
        else:
            print("Push failed.")
            return False

    except subprocess.CalledProcessError as e:
        print("Git command failed:", e.stderr if hasattr(e, 'stderr') else str(e))
        return False

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
        return {"Solutions": json.load(open(SOLUTION_LOG_PATH)) if SOLUTION_LOG_PATH.exists() else []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load Solutions log: {e}")


@api_router.get("/solution/latest")
def get_latest_solution():
    try:
        data = json.load(open(SOLUTION_LOG_PATH)) if SOLUTION_LOG_PATH.exists() else []
        return {"Solutions": data[-1] if data else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load latest Solutions: {e}")


@api_router.get("/solution/file/{filename}")
def get_solution_by_file(filename: str):
    try:
        data = json.load(open(SOLUTION_LOG_PATH)) if SOLUTION_LOG_PATH.exists() else []
        return {"Solutions": [e for e in data if filename in e.get("file", "")]}
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
    success = push_to_github()
    if success:
        return {"message": "GitHub push successful."}
    else:
        raise HTTPException(status_code=500, detail="GitHub push failed. See server logs for details.")


# ---------- Include Router ----------
app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("launcher:app", host="0.0.0.0", port=5000, reload=True)
