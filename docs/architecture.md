# Architecture

## Overview

AgentForge uses a hub-and-spoke model:

```
User Request → Orchestrator → Researcher → Analyst → Writer → Output
```

## Data Flow

1. User submits a task via the web UI or API
2. Orchestrator parses the task and selects a workflow
3. Agents execute in sequence, passing context forward
4. Each agent's output is logged for the execution timeline
5. Final output is returned to the user

## Adding New Agents

1. Define the agent in `agents.py`
2. Add it to a workflow in `orchestrator.py`
3. Create a prompt template in `prompts/`
