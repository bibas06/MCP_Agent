from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="GitHub Tools MCP Server")
mcp = FastMCP("github-tools")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "GitHub Tools MCP Server",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health",
        "mcp_endpoint": "/mcp",
        "available_tools": [
            "search_repositories(query) - Search GitHub repositories"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "github_token_configured": bool(GITHUB_TOKEN),
        "github_token_valid": "Check your .env file if False"
    }

@mcp.tool()
def search_repositories(query: str):
    """
    Search GitHub repositories
    
    Args:
        query: The search query (e.g., "python", "machine learning", "fastapi")
    
    Returns:
        List of top 5 repositories matching the query
    """
    try:
        url = "https://api.github.com/search/repositories"
        
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        
        params = {"q": query, "sort": "stars", "order": "desc", "per_page": 5}
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            repos = []
            
            for repo in data.get("items", []):
                repos.append({
                    "name": repo["full_name"],
                    "url": repo["html_url"],
                    "stars": repo["stargazers_count"],
                    "description": repo["description"],
                    "language": repo["language"]
                })
            
            return repos
        else:
            return {"error": f"GitHub API error: {response.status_code}", "message": response.text}
            
    except Exception as e:
        return {"error": str(e)}

app.mount("/mcp", mcp.sse_app())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
