from datetime import datetime as dt
from json import dump as dump_json
from json import load as load_json
from pathlib import Path
from typing import Final, Iterator

from util._types import JSONArr, JSONObj, StatusCode


class SessionData:
    FILE: Final[Path] = Path("data/sessions.json")

    device_id: str
    data: JSONArr

    def __init__(self, device_id: str) -> None:
        self.device_id = device_id
        self.data = self._load()

    @property
    def total_count(self) -> int:
        return len(self.data)

    @property
    def total_dur(self) -> int:
        return sum([session.get("duration_mins", 0) for session in self.data])

    @property
    def avg_dur(self) -> float:
        count: int = self.total_count
        return self.total_dur / count if count > 0 else 0

    def add_ses(self, data: JSONObj) -> StatusCode:
        device_id: str | None = data.get("device_id", None)
        if device_id is None:
            return StatusCode.MISSING_DEVICE_ID

        if device_id != self.device_id:
            return StatusCode.INVALID_DEVICE_ID

        for ses in self.data:
            if ses["status"] == "active":
                return StatusCode.ACTIVE_SESSION_EXISTS

        session = {
            "id": self.total_count + 1,
            "device_id": device_id,
            "start_time": dt.now().isoformat(),
            "status": "active",
            "meows": 0,
            "purrs": 0,
            "hisses": 0,
        }

        self.data.append(session)
        self.save()
        return StatusCode.SUCCESS

    def update_ses(self, data: JSONObj) -> StatusCode:
        device_id: str | None = data.get("device_id", None)
        if device_id is None:
            return StatusCode.MISSING_DEVICE_ID

        if device_id != self.device_id:
            return StatusCode.INVALID_DEVICE_ID

        sound: str | None = data.get("sound", None)
        if sound is None:
            return StatusCode.MISSING_SOUND

        if sound not in ("meow", "purr", "hiss"):
            return StatusCode.INVALID_SOUND

        sound += "es" if sound == "hiss" else "s"
        for ses in self.data:
            if ses["status"] == "active":
                ses[sound] += 1

                self.save()
                return StatusCode.SUCCESS

        return StatusCode.NO_ACTIVE_SESSION

    def end_ses(self, data: JSONObj) -> StatusCode:
        device_id: str | None = data.get("device_id", None)
        if device_id is None:
            return StatusCode.MISSING_DEVICE_ID

        if device_id != self.device_id:
            return StatusCode.INVALID_DEVICE_ID

        for ses in self.data:
            if ses["status"] == "active":
                ses["status"] = "completed"
                ses["end_time"] = dt.now().isoformat()

                start: dt = dt.fromisoformat(ses["start_time"])
                end: dt = dt.fromisoformat(ses["end_time"])
                duration: float = (end - start).total_seconds() / 60
                ses["duration_mins"] = round(duration, 1)

                self.save()
                return StatusCode.SUCCESS

        return StatusCode.NO_ACTIVE_SESSION

    def _load(self) -> JSONArr:
        with SessionData.FILE.open(encoding="utf-8") as file:
            data: JSONArr = load_json(file)
            for ses in data:
                if ses["device_id"] != self.device_id:
                    raise ValueError("Invalid device ID session JSON")
            return data

    def save(self) -> None:
        with SessionData.FILE.open("w") as file:
            dump_json(self.data, file)

    def __iter__(self) -> Iterator[JSONObj]:
        return iter(self.data)
