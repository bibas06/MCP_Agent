#run ./run_servers.sh to start all MCP servers and the FastAPI Gateway

echo "Starting MCP servers..."

uvicorn mcp_servers.github_server:app --port 8001 --reload &
uvicorn mcp_servers.perplexity_server:app --port 8002 --reload &
uvicorn mcp_servers.calendar_server:app --port 8003 --reload &

echo "Starting FastAPI Gateway..."

uvicorn api.gateway:app --port 8000 --reload