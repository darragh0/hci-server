from json import dump as dump_json
from json import load as load_json
from pathlib import Path
from typing import Final

from util._types import JSONArr, JSONObj


class SessionData:
    FILE: Final[Path] = Path("data/sessions.json")

    data: JSONArr

    def __init__(self):
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

    def add(self, session: JSONObj):
        self.data.append(session)
        self.save()

    def _load(self):
        with SessionData.FILE.open(encoding="utf-8") as file:
            return load_json(file)

    def save(self):
        with SessionData.FILE.open("w") as file:
            dump_json(self.data, file)

    def __iter__(self):
        return iter(self.data)
