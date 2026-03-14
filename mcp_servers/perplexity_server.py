from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
mcp = FastMCP("perplexity-tools")

API_KEY = os.getenv("PERPLEXITY_API_KEY")

@mcp.tool()
def web_search(query: str):
    """
    Search the web using Perplexity
    """

    url = "https://api.perplexity.ai/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "sonar-small-online",
        "messages": [
            {"role": "user", "content": query}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()

    return data["choices"][0]["message"]["content"]


app.mount("/mcp", mcp.sse_app())