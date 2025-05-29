import os
import yaml

def require_env(var_name):
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value
    
def load_config(path="koyeb-config.yaml"):
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    # Use the helper to ensure variables are present
    db_user = require_env("DATABASE_USER")
    db_password = require_env("DATABASE_PASSWORD")
    db_host = require_env("DATABASE_HOST")
    db_name = require_env("DATABASE_NAME")

    # Safely build config values from env vars
    config["common"]["port"] = int(os.getenv("PORT", 8080))  # optional default
    config["postgres"]["database_url"] = f"postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}"

    return config