from os import environ

import yaml

CONFIG_PATH = environ.get("CONFIG_PATH", "../assets/config.yaml")


def load_config():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


config = load_config()
