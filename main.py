from flask import request

from util import App, JSONObj, SessionData, StatusCode

app: App = App("Anti-Pawcrastinator")
ses_data: SessionData = SessionData("anti-pawcrastinator")


@app.route("/", methods=["GET"])
def html() -> str:
    return app.html(
        "index.html",
        request=request,
        total_sessions=ses_data.total_count,
        total_dur=ses_data.total_dur,
        avg_dur=ses_data.avg_dur,
        sessions=ses_data,
    )


@app.route("/api/session/start", methods=["POST"])
def start_ses() -> JSONObj:
    data = request.get_json()
    status: StatusCode = ses_data.add_ses(data)

    return app.response(status)


@app.route("/api/session/end", methods=["POST"])
def end_ses() -> JSONObj:
    data: JSONObj = request.get_json()
    status: StatusCode = ses_data.end_ses(data)

    return app.response(status)


@app.route("/api/session/sound", methods=["POST"])
def update_ses() -> JSONObj:
    data: JSONObj = request.get_json()
    status: StatusCode = ses_data.update_ses(data)

    return app.response(status)


@app.route("/api/session/active", methods=["GET"])
def get_active_session() -> JSONObj:
    for ses in ses_data:
        if ses["status"] == "active":
            return {"session": ses}
    return {"session": None}


@app.route("/api/session/all", methods=["GET"])
def get_all_sessions() -> JSONObj:
    return {"sessions": ses_data.data}


if __name__ == "__main__":
    app.run()
