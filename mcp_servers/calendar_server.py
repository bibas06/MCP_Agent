from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Google Calendar MCP Server")
mcp = FastMCP("calendar-tools")

API_KEY = os.getenv("GOOGLE_API_KEY")
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")

@app.get("/")
async def root():
    """Welcome endpoint"""
    return {
        "message": "Google Calendar MCP Server",
        "version": "1.0.0",
        "description": "MCP server for accessing Google Calendar events",
        "documentation": "/docs",
        "health_check": "/health",
        "mcp_endpoint": "/mcp",
        "available_tools": [
            "get_events() - Get upcoming calendar events (max 5)"
        ],
        "configuration": {
            "calendar_id_configured": bool(CALENDAR_ID),
            "api_key_configured": bool(API_KEY)
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    connection_status = "unknown"
    try:
        if API_KEY and CALENDAR_ID:
            service = build("calendar", "v3", developerKey=API_KEY)
            service.events().list(
                calendarId=CALENDAR_ID,
                maxResults=1
            ).execute()
            connection_status = "connected"
        else:
            connection_status = "missing_credentials"
    except Exception as e:
        connection_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "google_api_key_configured": bool(API_KEY),
        "calendar_id_configured": bool(CALENDAR_ID),
        "connection_status": connection_status,
        "timestamp": str(os.times().elapsed)
    }

if not API_KEY or not CALENDAR_ID:
    print("⚠️  Warning: GOOGLE_API_KEY or GOOGLE_CALENDAR_ID not set in .env file")
    print("Please create a .env file with:")
    print("GOOGLE_API_KEY=your_api_key_here")
    print("GOOGLE_CALENDAR_ID=your_calendar_id_here")

service = build("calendar", "v3", developerKey=API_KEY)

@mcp.tool()
def get_events():
    """
    Get upcoming calendar events
    
    Returns a list of the next 5 upcoming events from your Google Calendar.
    Each event includes the summary/title and start time.
    
    Returns:
        List of events with summary and start time
    """
    try:
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            maxResults=5,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])
        result = []

        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            
            result.append({
                "summary": event.get("summary"),
                "start": start,
                "html_link": event.get("htmlLink", ""),
                "creator": event.get("creator", {}).get("email", "")
            })

        return {
            "event_count": len(result),
            "events": result,
            "calendar_id": CALENDAR_ID
        }
    
    except Exception as e:
        return {
            "error": str(e),
            "message": "Failed to fetch calendar events. Check your API key and calendar ID."
        }

app.mount("/mcp", mcp.sse_app())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
