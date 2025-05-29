import os
import yaml

def load_config(path="koyeb-config.yaml"):
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    # Inject environment variables
    config["common"]["port"] = int(os.getenv("PORT", 8080))
    config["postgres"]["database_url"] = (
        f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
        f"@{os.getenv('DATABASE_HOST')}:5432/{os.getenv('DATABASE_NAME')}"
    )

    return config