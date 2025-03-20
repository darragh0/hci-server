from enum import IntEnum
from typing import Any, TypeAlias

JSONVal: TypeAlias = Any
JSONArr: TypeAlias = list[JSONVal]
JSONObj: TypeAlias = dict[str, JSONVal]


class StatusCode(IntEnum):
    SUCCESS = 0
    MISSING_DEVICE_ID = 1
    INVALID_DEVICE_ID = 2
    MISSING_SOUND = 3
    INVALID_SOUND = 4
    NO_ACTIVE_SESSION = 5
    ACTIVE_SESSION_EXISTS = 6
