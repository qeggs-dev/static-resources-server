from pathlib import Path
from fastapi import HTTPException
from fastapi.responses import FileResponse
from .._is_validate_path import validate_path
from .._configs import GlobalConfigManager
from ._app import app
from loguru import logger

@app.get("/{static_file:path}")
async def get_file(static_file: str):
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
    return FileResponse(base_path / static_file)