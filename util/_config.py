from dataclasses import dataclass


@dataclass
class Config:
    host: str = "0.0.0.0"
    port: int = 8080


def get_config() -> Config:
    return Config()
