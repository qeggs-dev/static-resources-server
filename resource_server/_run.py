import json
import uvicorn

from pathlib import Path
from loguru import logger
from ._app import app
from ._logger_init import logger_init
from ._configs import GlobalConfigManager, Configs

def load_configs():
    config_dir = Path("./configs")
    config_files: list[Path] = []
    for file in config_dir.glob("*.json"):
        config_files.append(file)
    
    if len(config_files) == 0:
        logger.warning("No config files found in configs directory, creating default config file...")
        config_file = config_dir / "default.json"
        with open(config_file, "w", encoding="utf-8") as file:
            configs = Configs()
            json.dump(configs.model_dump(), file, indent=4, ensure_ascii=False)
    elif len(config_files) == 1:
        config_file: Path = config_files[0]
    else:
        for index, file in enumerate(config_files):
            print(f"{index}: {file.name}")
        while True:
            try:
                choice = int(input("Choose a config file: "))
                config_file = config_files[choice]
                break
            except ValueError:
                logger.error("Invalid choice")
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as file:
            configs = Configs(**json.load(file))
    else:
        logger.error("Config file {config_file} does not exist", config_file = config_file)
    return configs

def run():
    try:
        configs = load_configs()
        logger_init(configs.logger)
        GlobalConfigManager.set_configs(configs)

        uvicorn.run(
            app,
            host = configs.host,
            port = configs.port,
            log_config = None
        )
    except Exception as e:
        logger.exception(e)