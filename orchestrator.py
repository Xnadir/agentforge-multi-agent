"""
Orchestrator — routes tasks through a pipeline of agents.
Supports predefined workflows and custom agent chains.
"""

import time
from datetime import datetime
from agents import get_agent, list_agents


# predefined workflows
WORKFLOWS = {
    "research_report": {
        "name": "Research & Report",
        "description": "Research a topic, analyze findings, and write a polished report",
        "agents": ["researcher", "analyst", "writer"],
    },
    "code_review": {
        "name": "Code Review",
        "description": "Analyze code, find bugs, and suggest improvements",
        "agents": ["coder", "critic"],
    },
    "content_creation": {
        "name": "Content Creation",
        "description": "Research, write, and review content for any purpose",
        "agents": ["researcher", "writer", "critic"],
    },
    "deep_analysis": {
        "name": "Deep Analysis",
        "description": "Research, analyze data, review for quality",
        "agents": ["researcher", "analyst", "critic"],
    },
}


def run_workflow(task: str, workflow_id: str) -> dict:
    """Execute a predefined workflow — agents run in sequence, each passing context to the next."""
    workflow = WORKFLOWS.get(workflow_id)
    if not workflow:
        return {"error": f"Unknown workflow: {workflow_id}"}

    start_time = time.time()
    steps = []
    context = ""

    for agent_id in workflow["agents"]:
        agent = get_agent(agent_id)
        if not agent:
            continue

        step_start = time.time()
        result = agent.execute(task, context=context)
        step_time = round(time.time() - step_start, 2)

        result["time_seconds"] = step_time
        steps.append(result)

        # pass this agent's output as context for the next one
        if result["status"] == "success":
            context += f"\n\n--- Output from {agent.name} ({agent.role}) ---\n{result['output']}"

    total_time = round(time.time() - start_time, 2)

    return {
        "workflow": workflow["name"],
        "task": task,
        "steps": steps,
        "total_time": total_time,
        "timestamp": datetime.now().isoformat(),
        "agent_count": len(steps),
    }


def run_custom_chain(task: str, agent_ids: list) -> dict:
    """Run a custom chain of agents."""
    start_time = time.time()
    steps = []
    context = ""

    for agent_id in agent_ids:
        agent = get_agent(agent_id)
        if not agent:
            steps.append({"agent": agent_id, "status": "error", "output": f"Agent '{agent_id}' not found"})
            continue

        step_start = time.time()
        result = agent.execute(task, context=context)
        result["time_seconds"] = round(time.time() - step_start, 2)
        steps.append(result)

        if result["status"] == "success":
            context += f"\n\n--- Output from {agent.name} ({agent.role}) ---\n{result['output']}"

    return {
        "workflow": "Custom Chain",
        "task": task,
        "steps": steps,
        "total_time": round(time.time() - start_time, 2),
        "timestamp": datetime.now().isoformat(),
        "agent_count": len(steps),
    }


def get_workflows():
    return [{"id": k, **v} for k, v in WORKFLOWS.items()]
