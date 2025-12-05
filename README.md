# AgentForge — Multi-Agent AI System 🤖

A system where multiple AI agents work together to solve complex tasks. Give it a job — like "research a topic and write a report" — and watch the agents collaborate.

Each agent has a specific role: Researcher finds information, Analyst processes it, and Writer creates the final output. They pass work between each other just like a real team.

## Features

- **3 specialized agents** — Researcher, Analyst, Writer
- **Task delegation** — agents pass context between each other
- **Tool use** — agents can search the web and analyze data
- **Live execution log** — watch agents think and work in real-time
- **Multiple workflows** — research, code review, content creation
- Customizable agent prompts
- Full execution history

## Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/agentforge-multi-agent.git
cd agentforge-multi-agent

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

echo GEMINI_API_KEY=your_key_here > .env

python app.py
```

Open `http://localhost:8000`. Try the "Research & Report" workflow.

## How It Works

```
User Task → Orchestrator → Agent 1 (Research) → Agent 2 (Analyze) → Agent 3 (Write) → Final Output
                              ↓                    ↓                    ↓
                         Tool Calls            Processing           Formatting
```

1. **Orchestrator** breaks down the task and assigns it to agents
2. **Researcher** gathers information (web search simulation + knowledge)
3. **Analyst** processes and structures the raw findings
4. **Writer** produces the final polished output
5. Each step is logged and visible in the execution timeline

## Tech Stack

- **Backend:** Python, FastAPI
- **AI:** Google Gemini API
- **Frontend:** HTML, CSS, JavaScript

## Project Structure

```
agentforge-multi-agent/
├── app.py              # FastAPI server
├── agents.py           # Agent definitions and execution
├── orchestrator.py     # Task routing and delegation
├── requirements.txt
├── .env.example
├── static/
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── README.md
```

## License

MIT
