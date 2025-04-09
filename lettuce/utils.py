import yaml
from pathlib import Path


def load_yaml_config(path="lettuce.yml"):
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"No config file found at {config_path}")
    with config_path.open() as f:
        return yaml.safe_load(f)


def expand_path(path):
    return str(Path(path).expanduser().resolve())


def get_watch_paths(config):
    return [expand_path(config.get("source", "."))]
