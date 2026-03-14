from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
mcp = FastMCP("calendar-tools")

API_KEY = os.getenv("GOOGLE_API_KEY")
CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")

service = build("calendar", "v3", developerKey=API_KEY)

@mcp.tool()
def get_events():
    """
    Get upcoming calendar events
    """

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        maxResults=5,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    result = []

    for event in events:
        result.append({
            "summary": event.get("summary"),
            "start": event["start"].get("dateTime", event["start"].get("date"))
        })

    return result


app.mount("/mcp", mcp.sse_app())