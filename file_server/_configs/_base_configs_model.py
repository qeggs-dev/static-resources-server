from pydantic import BaseModel, Field
from ._logger import LoggerConfig

class Configs(BaseModel):
    # server configs
    host: str = "0.0.0.0"
    port: int = 8000

    base_path: str = "./static"
    logger: LoggerConfig = Field(default_factory=LoggerConfig)