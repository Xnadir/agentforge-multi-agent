"""
Agents — defines specialized AI agents with roles, tools, and execution logic.
Each agent has a specific personality and skill set.
"""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


class Agent:
    """Base agent class with a role, goal, and backstory."""

    def __init__(self, name: str, role: str, goal: str, backstory: str, tools: list = None):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.tools = tools or []
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def execute(self, task: str, context: str = "") -> dict:
        """Run the agent on a task. Returns the agent's output and thinking."""
        prompt = f"""You are {self.name}, a {self.role}.

YOUR GOAL: {self.goal}

BACKSTORY: {self.backstory}

{f"CONTEXT FROM PREVIOUS AGENTS:{chr(10)}{context}" if context else ""}

YOUR TASK: {task}

Provide a thorough, well-structured response. Use markdown formatting.
Think step by step, then deliver your output."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(temperature=0.4, max_output_tokens=4096)
            )
            return {
                "agent": self.name,
                "role": self.role,
                "output": response.text,
                "status": "success"
            }
        except Exception as e:
            return {
                "agent": self.name,
                "role": self.role,
                "output": f"Agent error: {str(e)}",
                "status": "error"
            }


# Pre-defined agent team
AGENTS = {
    "researcher": Agent(
        name="Nova",
        role="Senior Research Analyst",
        goal="Find comprehensive, accurate information on any topic",
        backstory="You're a seasoned researcher with 10+ years of experience in data gathering and analysis. You excel at finding key insights, identifying trends, and synthesizing information from multiple sources. You always cite your reasoning and provide well-organized findings.",
    ),
    "analyst": Agent(
        name="Atlas",
        role="Data Analyst & Strategist",
        goal="Process raw research into actionable insights and structured analysis",
        backstory="You're an expert data analyst who turns messy information into clear, structured insights. You identify patterns, assess risks and opportunities, compare options, and provide data-driven recommendations. You use tables and bullet points to organize your analysis.",
    ),
    "writer": Agent(
        name="Echo",
        role="Content Writer & Editor",
        goal="Produce polished, engaging content from analyzed data",
        backstory="You're a skilled writer who creates clear, compelling content. You can write blog posts, reports, summaries, and technical documentation. You focus on readability, flow, and making complex topics accessible. You always produce well-structured, publication-ready content.",
    ),
    "coder": Agent(
        name="Bolt",
        role="Software Engineer",
        goal="Write clean, well-documented code and technical solutions",
        backstory="You're a full-stack software engineer who writes clean, efficient code. You can design architectures, review code for bugs, write tests, and explain technical concepts. You always include comments and follow best practices.",
    ),
    "critic": Agent(
        name="Sage",
        role="Quality Reviewer & Fact-Checker",
        goal="Review work for accuracy, completeness, and quality",
        backstory="You're a meticulous reviewer who catches errors, identifies gaps, and ensures quality. You check facts, evaluate arguments, and provide constructive feedback. You rate the overall quality and suggest specific improvements.",
    ),
}

def get_agent(agent_id: str) -> Agent:
    return AGENTS.get(agent_id)

def list_agents() -> list:
    return [{"id": k, "name": v.name, "role": v.role, "goal": v.goal} for k, v in AGENTS.items()]
