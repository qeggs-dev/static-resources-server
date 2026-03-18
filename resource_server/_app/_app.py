from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from loguru import logger
from typing import Callable, Awaitable

app = FastAPI(
    title = "Static Resource Server",
    description="A simple static resource server",
    version="1.0.0",
)

@app.middleware("http")
async def http_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception(e)
        response = JSONResponse(
            {
                "message": "Internal Server Error"
            }
        )
    return response