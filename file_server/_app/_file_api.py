from pathlib import Path
from fastapi import HTTPException
from fastapi.responses import FileResponse
from .._is_validate_path import validate_path
from .._configs import GlobalConfigManager
from ._app import app

@app.get("/{static_file}")
async def get_file(static_file: str):
    base_path =  Path(GlobalConfigManager.get_configs().base_path)
    if not validate_path(base_path, static_file):
        raise HTTPException(status_code=400, detail="Invalid path")
    
    return FileResponse(base_path / static_file)