from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
mcp = FastMCP("github-tools")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@mcp.tool()
def search_repositories(query: str):
    """
    Search GitHub repositories
    """

    url = "https://api.github.com/search/repositories"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    params = {"q": query, "sort": "stars", "order": "desc"}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    repos = []

    for repo in data.get("items", [])[:5]:
        repos.append({
            "name": repo["full_name"],
            "url": repo["html_url"],
            "stars": repo["stargazers_count"],
            "description": repo["description"]
        })

    return repos


app.mount("/mcp", mcp.sse_app())