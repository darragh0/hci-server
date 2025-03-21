from typing import Any

from flask import Flask, render_template
from flask_cors import CORS

from util._types import JSONObj, StatusCode


class App(Flask):
    def __init__(self, import_name: str):
        super().__init__(import_name=import_name)

        # Enable CORS
        CORS(
            self,
            origins=["*"],
            supports_credentials=True,
            methods=["*"],
            allow_headers=["*"],
        )

        # Register error handlers
        self.register_error_handler(404, self.not_found_handler)

    def html(self, file: str, **kwargs) -> str:
        return render_template(file, **kwargs)

    def run(self, debug=True, port=5000):
        """Run the application on all interfaces (0.0.0.0)"""
        super().run(host='0.0.0.0', port=port, debug=debug)

    def _err(self, msg: str) -> JSONObj:
        return {"status": "error", "message": msg}

    def _success(self) -> JSONObj:
        return {"status": "success"}

    def response(self, code: StatusCode) -> JSONObj:
        match code:
            case StatusCode.SUCCESS:
                return self._success()
            case StatusCode.MISSING_DEVICE_ID:
                return self._err("Missing device_id")
            case StatusCode.INVALID_DEVICE_ID:
                return self._err("Invalid device_id")
            case StatusCode.NO_ACTIVE_SESSION:
                return self._err("No active session found")
            case StatusCode.INVALID_SOUND:
                return self._err("Invalid sound. Must be 'meow', 'purr', or 'hiss")
            case StatusCode.ACTIVE_SESSION_EXISTS:
                return self._err("Active session already exists")
            case _:
                return self._err("Unknown error")

    def not_found_handler(self, _: Any) -> tuple[str, int]:
        return render_template("404.html"), 404
