import os
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_groq import ChatGroq
from src.config import MODEL_NAME, GROQ_API_KEY, TEMPERATURE
from src.prompts import get_agent_prompt
from src.tools import get_expenses_count, get_all_expenses, add_expense

def create_finance_agent():
    """Create and return the finance agent."""

    os.environ["GROQ_API_KEY"] = GROQ_API_KEY

    llm = ChatGroq(model=MODEL_NAME, temperature=TEMPERATURE)

    tools = [get_expenses_count, get_all_expenses, add_expense]
    prompt = get_agent_prompt()
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    return agent_executor