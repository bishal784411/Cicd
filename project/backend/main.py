"""
DevOps Control Center API - Multi-page Dashboard Backend
Serves monitoring data, solutions management, and agent control
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import uvicorn
from pydantic import BaseModel
import random
import uuid

app = FastAPI(title="DevOps Control Center API", version="2.0.0")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to error log file
ERROR_LOG_PATH = "error_log.json"

class FixRequest(BaseModel):
    file: str
    error_index: int

def generate_mock_system_metrics() -> Dict[str, Any]:
    """Generate realistic system metrics for demo purposes"""
    return {
        "cpu_usage": random.randint(15, 85),
        "memory_usage": random.randint(30, 90),
        "disk_usage": random.randint(20, 75),
        "network_latency": random.randint(5, 50),
        "active_monitors": random.randint(8, 25),
        "fixes_applied_today": random.randint(3, 15)
    }

def generate_mock_solutions() -> List[Dict[str, Any]]:
    """Generate mock solutions data"""
    solutions = [
        {
            "id": str(uuid.uuid4()),
            "name": "XSS Vulnerability Fixer",
            "description": "Automatically sanitizes user input to prevent cross-site scripting attacks",
            "category": "security",
            "status": "active",
            "success_rate": 95,
            "last_executed": (datetime.now() - timedelta(hours=2)).isoformat(),
            "execution_count": 47,
            "avg_execution_time": 3.2,
            "error_types": ["SECURITY", "HTML"],
            "auto_trigger": True,
            "created_by": "security-team",
            "created_at": (datetime.now() - timedelta(days=30)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "CSS Optimization Engine",
            "description": "Minifies and optimizes CSS files to reduce load times",
            "category": "performance",
            "status": "active",
            "success_rate": 88,
            "last_executed": (datetime.now() - timedelta(minutes=30)).isoformat(),
            "execution_count": 156,
            "avg_execution_time": 8.7,
            "error_types": ["CSS", "PERFORMANCE"],
            "auto_trigger": True,
            "created_by": "performance-team",
            "created_at": (datetime.now() - timedelta(days=45)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Database Connection Pool Manager",
            "description": "Manages database connections and implements retry logic",
            "category": "configuration",
            "status": "active",
            "success_rate": 92,
            "last_executed": (datetime.now() - timedelta(hours=1)).isoformat(),
            "execution_count": 23,
            "avg_execution_time": 12.4,
            "error_types": ["JS", "CONFIG"],
            "auto_trigger": False,
            "created_by": "backend-team",
            "created_at": (datetime.now() - timedelta(days=15)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "SSL Certificate Renewal",
            "description": "Automatically renews SSL certificates before expiration",
            "category": "maintenance",
            "status": "inactive",
            "success_rate": 100,
            "last_executed": (datetime.now() - timedelta(days=7)).isoformat(),
            "execution_count": 12,
            "avg_execution_time": 45.2,
            "error_types": ["CONFIG", "SECURITY"],
            "auto_trigger": True,
            "created_by": "devops-team",
            "created_at": (datetime.now() - timedelta(days=60)).isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Memory Leak Detector",
            "description": "Identifies and fixes memory leaks in React components",
            "category": "performance",
            "status": "pending",
            "success_rate": 76,
            "last_executed": (datetime.now() - timedelta(hours=6)).isoformat(),
            "execution_count": 34,
            "avg_execution_time": 15.8,
            "error_types": ["JS", "PERFORMANCE"],
            "auto_trigger": False,
            "created_by": "frontend-team",
            "created_at": (datetime.now() - timedelta(days=20)).isoformat()
        }
    ]
    return solutions

def generate_mock_agents() -> List[Dict[str, Any]]:
    """Generate mock agents data"""
    agents = [
        {
            "id": str(uuid.uuid4()),
            "name": "Monitor-Agent-01",
            "type": "monitor",
            "status": "online",
            "health": "healthy",
            "last_heartbeat": datetime.now().isoformat(),
            "uptime": 99.8,
            "cpu_usage": random.randint(10, 40),
            "memory_usage": random.randint(20, 60),
            "tasks_completed": 1247,
            "tasks_failed": 3,
            "version": "v2.1.4",
            "location": "us-east-1",
            "capabilities": ["file-monitoring", "error-detection", "health-checks"],
            "current_task": "Scanning /src/components for errors",
            "queue_size": 5
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Fix-Agent-01",
            "type": "fix",
            "status": "busy",
            "health": "healthy",
            "last_heartbeat": (datetime.now() - timedelta(seconds=30)).isoformat(),
            "uptime": 97.2,
            "cpu_usage": random.randint(40, 80),
            "memory_usage": random.randint(50, 85),
            "tasks_completed": 892,
            "tasks_failed": 12,
            "version": "v1.8.2",
            "location": "us-west-2",
            "capabilities": ["auto-fix", "code-patching", "dependency-updates"],
            "current_task": "Applying XSS fix to UserAuth.tsx",
            "queue_size": 2
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Analysis-Agent-01",
            "type": "analysis",
            "status": "online",
            "health": "warning",
            "last_heartbeat": datetime.now().isoformat(),
            "uptime": 94.5,
            "cpu_usage": random.randint(20, 50),
            "memory_usage": random.randint(60, 90),
            "tasks_completed": 2156,
            "tasks_failed": 45,
            "version": "v3.0.1",
            "location": "eu-west-1",
            "capabilities": ["ai-analysis", "pattern-recognition", "risk-assessment"],
            "current_task": None,
            "queue_size": 0
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Deploy-Agent-01",
            "type": "deployment",
            "status": "maintenance",
            "health": "healthy",
            "last_heartbeat": (datetime.now() - timedelta(minutes=5)).isoformat(),
            "uptime": 98.9,
            "cpu_usage": 0,
            "memory_usage": random.randint(10, 30),
            "tasks_completed": 567,
            "tasks_failed": 8,
            "version": "v2.3.0",
            "location": "us-central-1",
            "capabilities": ["deployment", "rollback", "environment-management"],
            "current_task": None,
            "queue_size": 0
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Monitor-Agent-02",
            "type": "monitor",
            "status": "error",
            "health": "critical",
            "last_heartbeat": (datetime.now() - timedelta(minutes=15)).isoformat(),
            "uptime": 87.3,
            "cpu_usage": 0,
            "memory_usage": 0,
            "tasks_completed": 734,
            "tasks_failed": 67,
            "version": "v2.0.8",
            "location": "ap-southeast-1",
            "capabilities": ["file-monitoring", "error-detection"],
            "current_task": None,
            "queue_size": 0
        }
    ]
    return agents

def load_error_log() -> Dict[str, Any]:
    """Load and parse the error log JSON file"""
    try:
        if not os.path.exists(ERROR_LOG_PATH):
            # Return empty structure with mock data if file doesn't exist
            return {
                "last_updated": datetime.now().isoformat(),
                "total_files": 0,
                "files_with_errors": 0,
                "critical_issues": 0,
                "system_health": "healthy",
                "agent_status": "active",
                "files": [],
                "metrics": generate_mock_system_metrics()
            }
        
        with open(ERROR_LOG_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Transform raw error log into DevOps monitoring format
        return transform_error_data(data)
        
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON in error log: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading error log: {str(e)}")

def transform_error_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Transform raw error log data into DevOps monitoring format"""
    errors = raw_data.get("errors", [])
    
    # Group errors by file
    files_dict = {}
    critical_count = 0
    
    for error in errors:
        file_path = error.get("file", "unknown")
        severity = error.get("severity", "medium")
        
        if severity == "critical":
            critical_count += 1
            
        if file_path not in files_dict:
            files_dict[file_path] = {
                "file": file_path,
                "status": "healthy",
                "last_checked": error.get("timestamp", datetime.now().isoformat()),
                "error_count": 0,
                "critical_count": 0,
                "errors": [],
                "uptime_percentage": random.randint(95, 100),
                "last_fix_attempt": None
            }
        
        # Enhanced error entry with fix capabilities
        enhanced_error = {
            "timestamp": error.get("timestamp", datetime.now().isoformat()),
            "file": file_path,
            "error_type": error.get("error_type", "UNKNOWN"),
            "line_number": error.get("line_number"),
            "message": error.get("message", "No message provided"),
            "ai_analysis": error.get("ai_analysis"),
            "severity": severity,
            "fix_suggestion": error.get("fix_suggestion", "Manual review recommended"),
            "auto_fixable": error.get("auto_fixable", random.choice([True, False])),
            "fix_applied": error.get("fix_applied", False),
            "fix_timestamp": error.get("fix_timestamp")
        }
        
        files_dict[file_path]["errors"].append(enhanced_error)
        files_dict[file_path]["error_count"] = len(files_dict[file_path]["errors"])
        
        # Count critical errors per file
        if severity == "critical":
            files_dict[file_path]["critical_count"] += 1
            files_dict[file_path]["status"] = "critical"
        elif files_dict[file_path]["status"] != "critical" and severity in ["high", "medium"]:
            files_dict[file_path]["status"] = "warning"
        elif files_dict[file_path]["status"] == "healthy":
            files_dict[file_path]["status"] = "warning" if files_dict[file_path]["error_count"] > 0 else "healthy"
    
    files_list = list(files_dict.values())
    files_with_errors = len([f for f in files_list if f["error_count"] > 0])
    
    # Determine system health
    system_health = "healthy"
    if critical_count > 0:
        system_health = "critical"
    elif files_with_errors > len(files_list) * 0.3:  # More than 30% have errors
        system_health = "degraded"
    
    # Determine agent status
    agent_status = "active"
    if critical_count > 5:
        agent_status = "error"
    elif len(files_list) == 0:
        agent_status = "idle"
    
    return {
        "last_updated": raw_data.get("last_updated", datetime.now().isoformat()),
        "total_files": len(files_list),
        "files_with_errors": files_with_errors,
        "critical_issues": critical_count,
        "system_health": system_health,
        "agent_status": agent_status,
        "files": files_list,
        "metrics": generate_mock_system_metrics()
    }

# Monitor endpoints
@app.get("/monitor/errors")
async def get_monitoring_errors():
    """Get current monitoring status with DevOps metrics"""
    try:
        data = load_error_log()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/monitor/fix")
async def trigger_fix(fix_request: FixRequest):
    """Trigger automated fix for a specific error"""
    try:
        print(f"Fix triggered for {fix_request.file}, error index {fix_request.error_index}")
        
        # Simulate fix processing time
        import time
        time.sleep(0.5)
        
        return {
            "status": "success",
            "message": f"Fix initiated for {fix_request.file}",
            "fix_id": f"fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "estimated_completion": (datetime.now()).isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fix request failed: {str(e)}")

@app.get("/monitor/metrics")
async def get_system_metrics():
    """Get real-time system metrics"""
    return generate_mock_system_metrics()

# Solutions endpoints
@app.get("/solutions")
async def get_solutions():
    """Get all available solutions"""
    try:
        solutions = generate_mock_solutions()
        return solutions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/solutions/{solution_id}/toggle")
async def toggle_solution(solution_id: str):
    """Toggle solution active/inactive status"""
    try:
        # In a real implementation, this would update the solution status
        print(f"Toggling solution {solution_id}")
        return {"status": "success", "message": f"Solution {solution_id} status toggled"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/solutions/{solution_id}/execute")
async def execute_solution(solution_id: str):
    """Execute a solution manually"""
    try:
        # In a real implementation, this would trigger the solution execution
        print(f"Executing solution {solution_id}")
        return {"status": "success", "message": f"Solution {solution_id} execution started"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Agents endpoints
@app.get("/agents")
async def get_agents():
    """Get all registered agents"""
    try:
        agents = generate_mock_agents()
        return agents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/{agent_id}/restart")
async def restart_agent(agent_id: str):
    """Restart an agent"""
    try:
        # In a real implementation, this would restart the agent
        print(f"Restarting agent {agent_id}")
        return {"status": "success", "message": f"Agent {agent_id} restart initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/{agent_id}/stop")
async def stop_agent(agent_id: str):
    """Stop an agent"""
    try:
        # In a real implementation, this would stop the agent
        print(f"Stopping agent {agent_id}")
        return {"status": "success", "message": f"Agent {agent_id} stop initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Enhanced health check with system status"""
    try:
        data = load_error_log()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "system_health": data.get("system_health", "unknown"),
            "agent_status": data.get("agent_status", "unknown"),
            "monitored_files": data.get("total_files", 0),
            "critical_issues": data.get("critical_issues", 0)
        }
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

if __name__ == "__main__":
    print("🚀 Starting DevOps Control Center API Server...")
    print(f"📁 Error log path: {os.path.abspath(ERROR_LOG_PATH)}")
    print("🌐 API available at: http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("🔧 DevOps Control Center ready!")
    print("📊 Monitor • 🛠️ Solutions • 🤖 Agents")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )