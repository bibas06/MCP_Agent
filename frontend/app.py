import streamlit as st
import asyncio
from agent.graph import agent_graph

st.set_page_config(page_title="MCP AI Agent")

st.title("Multi MCP LangGraph Assistant")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.chat_input("Ask something...")

async def run_agent(query):

    result = await agent_graph.ainvoke({
        "user_input": query,
        "tool_result": "",
        "final_answer": ""
    })

    return result["final_answer"]


if user_input:

    st.session_state.history.append(("user", user_input))

    answer = asyncio.run(run_agent(user_input))

    st.session_state.history.append(("assistant", answer))


for role, msg in st.session_state.history:

    if role == "user":
        with st.chat_message("user"):
            st.write(msg)

    else:
        with st.chat_message("assistant"):
            st.write(msg)