# MCP Agent — Multi-Tool LangGraph AI Assistant

A multi-agent AI system built with LangGraph, FastMCP, and Groq (LLaMA 3.3 70B). It routes user queries through specialized MCP servers for GitHub, web search, and Google Calendar, then synthesizes a final response via a Streamlit frontend.

---

## Architecture

```
User (Streamlit UI)
       │
       ▼
FastAPI Gateway  (port 8000)
       │
       ▼
LangGraph Agent
  ├── Planner      → decides which tool to use
  ├── Tool Executor → calls the right MCP server
  └── Responder    → generates final answer
       │
       ├── GitHub MCP Server    (port 8001)
       ├── Search MCP Server    (port 8002)  ← Tavily
       └── Calendar MCP Server  (port 8003)  ← Google Calendar
```

---

## Project Structure

```
MCP_Agent/
├── agent/
│   ├── graph.py        # LangGraph pipeline (planner → tool_executor → responder)
│   ├── model.py        # Groq LLM setup (LLaMA 3.3 70B)
│   └── state.py        # AgentState TypedDict
├── api/
│   └── gateway.py      # FastAPI gateway — exposes /chat, /health
├── frontend/
│   └── app.py          # Streamlit chat UI
├── mcp_client/
│   └── client.py       # MCP SSE client for calling tools
├── mcp_servers/
│   ├── github_server.py    # GitHub repository search
│   ├── search_server.py    # Tavily web search
│   └── calendar_server.py  # Google Calendar events
├── .env                # API keys (not committed)
├── requirements.txt
└── run_servers.sh      # Starts all servers
```

---

## Setup

### 1. Clone & install dependencies

```bash
git clone <repo-url>
cd MCP_Agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GITHUB_TOKEN=your_github_personal_access_token
TAVILY_API_KEY=your_tavily_api_key
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CALENDAR_ID=your_calendar_id
```

| Variable             | Where to get it |
|----------------------|-----------------|
| `GROQ_API_KEY`       | [console.groq.com](https://console.groq.com) |
| `GITHUB_TOKEN`       | GitHub → Settings → Developer Settings → PAT |
| `TAVILY_API_KEY`     | [tavily.com](https://tavily.com) |
| `GOOGLE_API_KEY`     | Google Cloud Console → APIs & Services |
| `GOOGLE_CALENDAR_ID` | Google Calendar → Settings → Calendar ID |

---

## Running the Project

### Option 1 — Shell script (Linux/Mac)

```bash
chmod +x run_servers.sh
./run_servers.sh
```

### Option 2 — Manual (Windows or step-by-step)

Open four separate terminals:

```bash
# Terminal 1 — GitHub MCP Server
uvicorn mcp_servers.github_server:app --port 8001 --reload

# Terminal 2 — Search MCP Server
uvicorn mcp_servers.search_server:app --port 8002 --reload

# Terminal 3 — Calendar MCP Server
uvicorn mcp_servers.calendar_server:app --port 8003 --reload

# Terminal 4 — API Gateway
uvicorn api.gateway:app --port 8000 --reload
```

Then start the frontend:

```bash
streamlit run frontend/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## API Endpoints

### Gateway (port 8000)

| Method | Endpoint  | Description              |
|--------|-----------|--------------------------|
| GET    | `/`       | Welcome + endpoint list  |
| GET    | `/health` | Health check             |
| POST   | `/chat`   | Send a query to the agent |

Example request:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Search GitHub for LangGraph projects"}'
```

### MCP Servers

| Server   | Port | Tool               | Description                        |
|----------|------|--------------------|------------------------------------|
| GitHub   | 8001 | `search_repositories` | Search GitHub repos by keyword  |
| Search   | 8002 | `web_search`          | Web search via Tavily            |
| Calendar | 8003 | `get_events`          | Fetch next 5 Google Calendar events |

Each server also exposes `/health` and `/docs` (Swagger UI).

---

## How It Works

The LangGraph pipeline runs three nodes in sequence:

1. **Planner** — sends the user query to LLaMA 3.3 70B and determines which tool to invoke (`github`, `perplexity`, or `calendar`).
2. **Tool Executor** — calls the appropriate MCP server via SSE using `MCPClient`.
3. **Responder** — takes the tool output and generates a final, user-friendly answer.

---

## Example Queries

- `"Search GitHub for FastAPI projects"` → GitHub search
- `"What are the latest AI news?"` → Tavily web search
- `"What's on my calendar this week?"` → Google Calendar events

---

## Requirements

- Python 3.10+
- All packages listed in `requirements.txt`
- Valid API keys for Groq, GitHub, Tavily, and Google Calendar
