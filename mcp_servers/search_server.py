from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

mcp = FastMCP("search-tools")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=TAVILY_API_KEY)


@mcp.tool()
def web_search(query: str):

    result = client.search(
        query=query,
        max_results=5
    )

    return result


app.mount("/mcp", mcp.sse_app())