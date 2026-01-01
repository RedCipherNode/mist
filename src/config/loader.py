import json
from pathlib import Path


DEFAULT_CONFIG = {
    "level": "medium",
    "passes": {
        "rename_identifiers": True,
        "string_obfuscation": False
    }
}


def load_config(config_path=None):
    config = DEFAULT_CONFIG.copy()
    config["passes"] = config["passes"].copy()

    if config_path is None:
        return config

    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        user_config = json.load(f)

    if "level" in user_config:
        config["level"] = user_config["level"]

    if "passes" in user_config:
        config["passes"].update(user_config["passes"])

    return config
