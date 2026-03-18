import aiofiles
from pathlib import Path
from fastapi import HTTPException, Query
from fastapi.responses import FileResponse, PlainTextResponse
from .._is_validate_path import validate_path
from .._configs import GlobalConfigManager
from ._app import app
from loguru import logger

@app.get("/{static_file:path}")
async def get_file(static_file: str, text_encoding: str | None = Query(None)):
    if not static_file:
        return FileResponse(
            GlobalConfigManager.get_configs().index_file,
            media_type="text/html"
        )
    base_path =  Path(GlobalConfigManager.get_configs().base_path)
    if not validate_path(base_path, static_file):
        raise HTTPException(status_code=400, detail="Invalid path")
    file = base_path / static_file
    logger.info(
        "Getting file: {file}",
        file = file.as_posix()
    )
    if not file.exists():
        raise HTTPException(status_code=404, detail="File not found")
    if text_encoding is not None:
        async with aiofiles.open(file, mode="r", encoding = text_encoding) as f:
            text = await f.read()
        return PlainTextResponse(text)
    return FileResponse(
        base_path / static_file
    )