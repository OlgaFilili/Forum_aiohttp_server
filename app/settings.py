import pathlib
import yaml
import os

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / "config" / "koyeb-config.yaml"


def get_config(path):
    with open(path) as f:
        parsed_config = yaml.safe_load(f)
        return parsed_config

def require_env(var_name):
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value
    
def load_config(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    # Use the helper to ensure variables are present
    db_user = require_env("POSTGRES_USER")
    db_password = require_env("POSTGRES_PASSWORD")
    db_host = require_env("POSTGRES_HOST")
    db_name = require_env("POSTGRES_NAME")
    
    # Safely build config values from env vars
    config["common"]["port"] = int(os.getenv("PORT", 8080))  # optional default
    config["postgres"]["database_url"] = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"

    return config
    
#config = get_config(config_path)
#config= load_config(config_path)
_config = None

def get_config():
    global _config
    if _config is None:
        _config = load_config(config_path)
    return _config