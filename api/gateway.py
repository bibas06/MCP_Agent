from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.graph import agent_graph

app = FastAPI(title="LangGraph MCP Gateway")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "LangGraph MCP Gateway",
        "version": "1.0.0",
        "endpoints": {
            "POST /chat": "Send chat messages to the agent",
            "GET /health": "Health check"
        },
        "frontend": "http://localhost:8501 (Streamlit UI)"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_loaded": agent_graph is not None
    }

@app.post("/chat")
async def chat(q: Query):
    """
    Chat with the MCP AI Agent
    
    Send a query and get a response from the agent.
    """
    try:
        result = await agent_graph.ainvoke({
            "user_input": q.query,
            "tool_result": "",
            "final_answer": ""
        })
        
        return {
            "response": result["final_answer"],
            "query": q.query
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to process query"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
