from fastapi import FastAPI
from pydantic import BaseModel
from agent.graph import agent_graph

app = FastAPI(title="LangGraph MCP Gateway")


class Query(BaseModel):
    query: str


@app.post("/chat")
async def chat(q: Query):

    result = await agent_graph.ainvoke(
        {
            "user_input": q.query,
            "tool_result": "",
            "final_answer": ""
        }
    )

    return {"response": result["final_answer"]}