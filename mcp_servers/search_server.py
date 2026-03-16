from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Tavily Search MCP Server")
mcp = FastMCP("search-tools")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Tavily Search MCP Server",
        "version": "1.0.0",
        "description": "MCP server for web search using Tavily API",
        "documentation": "/docs",
        "health_check": "/health",
        "mcp_endpoint": "/mcp",
        "available_tools": [
            "web_search(query) - Search the web and return top 5 results"
        ],
        "configuration": {
            "api_key_configured": bool(TAVILY_API_KEY)
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    connection_status = "unknown"
    try:
        if TAVILY_API_KEY:
            client = TavilyClient(api_key=TAVILY_API_KEY)
            test_result = client.search(query="test", max_results=1)
            connection_status = "connected"
        else:
            connection_status = "missing_api_key"
    except Exception as e:
        connection_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "tavily_api_key_configured": bool(TAVILY_API_KEY),
        "connection_status": connection_status,
        "timestamp": str(os.times().elapsed)
    }

if not TAVILY_API_KEY:
    print("⚠️  Warning: TAVILY_API_KEY not set in .env file")
    print("Please create a .env file with:")
    print("TAVILY_API_KEY=your_api_key_here")

client = TavilyClient(api_key=TAVILY_API_KEY)

@mcp.tool()
def web_search(query: str):
    """
    Search the web using Tavily API
    
    Performs a web search and returns the top 5 results with titles, URLs, and content snippets.
    
    Args:
        query: The search query string (e.g., "latest AI news", "Python tutorials")
    
    Returns:
        Dictionary with search results and metadata
    """
    try:
        if not TAVILY_API_KEY:
            return {
                "error": "Tavily API key not configured",
                "message": "Please set TAVILY_API_KEY in your .env file"
            }
        
        result = client.search(
            query=query,
            max_results=5,
            search_depth="basic"
        )
        
        formatted_results = []
        for item in result.get("results", []):
            formatted_results.append({
                "title": item.get("title", "No title"),
                "url": item.get("url", ""),
                "content": item.get("content", "")[:200] + "..." if len(item.get("content", "")) > 200 else item.get("content", ""),
                "score": item.get("score", 0)
            })
        
        return {
            "query": query,
            "result_count": len(formatted_results),
            "results": formatted_results,
            "response_time": result.get("response_time", 0)
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to perform search. Check your API key and try again.",
            "query": query
        }

app.mount("/mcp", mcp.sse_app())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
