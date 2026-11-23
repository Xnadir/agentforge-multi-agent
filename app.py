"""
AgentForge — FastAPI server for Multi-Agent System
Run with: python app.py
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from orchestrator import run_workflow, run_custom_chain, get_workflows
from agents import list_agents

app = FastAPI(title="AgentForge")
app.mount("/static", StaticFiles(directory="static"), name="static")


class TaskInput(BaseModel):
    task: str
    workflow_id: str = ""
    agent_ids: list[str] = []


@app.get("/")
async def home():
    return FileResponse("static/index.html")


@app.get("/api/agents")
async def get_agents():
    return {"agents": list_agents()}


@app.get("/api/workflows")
async def workflows():
    return {"workflows": get_workflows()}


@app.post("/api/run")
async def run(body: TaskInput):
    if not body.task.strip():
        raise HTTPException(400, "Task cannot be empty")

    if body.workflow_id:
        result = run_workflow(body.task.strip(), body.workflow_id)
    elif body.agent_ids:
        result = run_custom_chain(body.task.strip(), body.agent_ids)
    else:
        raise HTTPException(400, "Provide either a workflow_id or agent_ids")

    if "error" in result:
        raise HTTPException(400, result["error"])
    return result


if __name__ == "__main__":
    print("\n🤖 Starting AgentForge Multi-Agent System...")
    print("   Open http://localhost:8000 in your browser\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)

