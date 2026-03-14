#!/bin/bash

echo "🚀 Creating Multi MCP LangGraph Agent Project..."

PROJECT_NAME="MCP_Agent"

cd $PROJECT_NAME

# Root files
touch README.md
touch requirements.txt
touch .env.example
touch run_servers.sh

# Create folders
mkdir -p frontend
mkdir -p agent
mkdir -p mcp_client
mkdir -p mcp_servers

# Create files inside folders
touch frontend/app.py

touch agent/graph.py
touch agent/state.py
touch agent/model.py

touch mcp_client/client.py

touch mcp_servers/github_server.py
touch mcp_servers/perplexity_server.py
touch mcp_servers/calendar_server.py

echo "📁 Project structure created successfully!"

echo ""
echo "Structure:"
echo ""

tree .

echo ""
echo "Next steps:"
echo "1. Fill requirements.txt"
echo "2. Add API keys in .env"
echo "3. Start MCP servers"
echo "4. Run Streamlit UI"