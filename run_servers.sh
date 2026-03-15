echo "Starting MCP servers..."

uvicorn mcp_servers.github_server:app --port 8001 --reload &
uvicorn mcp_servers.search_server:app --port 8002 --reload &
uvicorn mcp_servers.calendar_server:app --port 8003 --reload &

echo "Starting FastAPI Gateway..."

uvicorn api.api_gateway:app --port 8000 --reload