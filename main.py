from datetime import datetime
from datetime import datetime as dt

from fastapi import Request
from fastapi.responses import HTMLResponse

from util import App, JSONObj, SessionData

app: App = App(title="Anti-Pawcrastinator", version="0.1.0")
ses_data: SessionData = SessionData()


@app.get("/", response_class=HTMLResponse)
async def html(request: Request) -> HTMLResponse:
    return app.html(
        "index.html",
        request=request,
        total_sessions=ses_data.total_count,
        total_dur=ses_data.total_dur,
        avg_dur=ses_data.avg_dur,
        sessions=ses_data,
    )


@app.post("/api/session/start")
async def start_ses(request: Request) -> JSONObj:
    data = await request.json()
    device_id = data.get("device_id", "default")

    # Create new session
    session = {
        "id": str(ses_data.total_count + 1),
        "device_id": device_id,
        "start_time": datetime.now().isoformat(),
        "status": "active",
    }

    ses_data.add(session)
    return app.success(session_id=session["id"])


@app.post("/api/session/end")
async def end_ses(request: Request) -> JSONObj:
    data: JSONObj = await request.json()
    device_id: str = data.get("device_id", "default")

    # Find active session for the device
    for ses in ses_data:
        if ses["device_id"] == device_id and ses["status"] == "active":
            ses["status"] = "completed"
            ses["end_time"] = datetime.now().isoformat()

            # Calculate duration
            start: dt = datetime.fromisoformat(ses["start_time"])
            end: dt = datetime.fromisoformat(ses["end_time"])
            duration: float = (end - start).total_seconds() / 60
            ses["duration_mins"] = round(duration, 1)

            ses_data.save()

            return {"status": "success", "session_id": ses["id"]}

    return app.err("No active session found for this device")


@app.get("/api/sessions")
async def get_sessions() -> JSONObj:
    return {"sessions": ses_data.data}


if __name__ == "__main__":
    app.run()
