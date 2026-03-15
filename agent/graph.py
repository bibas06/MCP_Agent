from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.model import get_llm
from mcp_client.client import MCPClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.state import AgentState  # Now this works

llm = get_llm()
client = MCPClient()


async def planner(state: AgentState):

    prompt = f"""
User Query: {state['user_input']}

Decide which tool to use:

github
search
calendar
none
"""

    res = await llm.ainvoke(prompt)

    return {"tool_result": res.content.strip().lower()}


async def tool_executor(state: AgentState):

    tool = state["tool_result"]
    query = state["user_input"]

    if tool == "github":

        result = await client.call_tool(
            "http://localhost:8001/mcp",
            "search_repositories",
            {"query": query}
        )

    elif tool == "perplexity":

        result = await client.call_tool(
            "http://localhost:8002/mcp",
            "web_search",
            {"query": query}
        )

    elif tool == "calendar":

        result = await client.call_tool(
            "http://localhost:8003/mcp",
            "get_events",
            {}
        )

    else:

        result = "No tool used"

    return {"tool_result": str(result)}


async def responder(state: AgentState):

    prompt = f"""
User Query:
{state['user_input']}

Tool Output:
{state['tool_result']}

Give a helpful response.
"""

    res = await llm.ainvoke(prompt)

    return {"final_answer": res.content}


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("planner", planner)
    graph.add_node("tool_executor", tool_executor)
    graph.add_node("responder", responder)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "tool_executor")
    graph.add_edge("tool_executor", "responder")
    graph.add_edge("responder", END)

    return graph.compile()


agent_graph = build_graph()