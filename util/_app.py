from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run as uvicorn_run

from util._config import Config, get_config
from util._types import JSONObj


class App(FastAPI):
    config: Config

    def __init__(self, title: str, version: str):
        super().__init__(title=title, version=version)

        # Enable CORS
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.config = get_config()
        self.mount("/static", StaticFiles(directory="static"), name="static")
        self.templates = Jinja2Templates(directory="templates")
        self.add_exception_handler(404, self.not_found_handler)

    def html(self, file: str, **kwargs):
        return self.templates.TemplateResponse(file, kwargs)

    def run(self) -> None:
        uvicorn_run(self, host=self.config.host, port=self.config.port)

    def err(self, msg: str) -> JSONObj:
        return {"status": "error", "message": msg}

    def success(self, **kwargs) -> JSONObj:
        return {"status": "success"} | kwargs

    async def not_found_handler(self, request: Request, _: Exception) -> HTMLResponse:
        return self.templates.TemplateResponse(
            "404.html", {"request": request}, status_code=404
        )
