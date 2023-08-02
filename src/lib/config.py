from os import environ

import yaml

from .constants import DEFAULT_CONFIG_PATH


class Config:
    __instance = None

    def __init__(self):
        self.config_path = environ.get("CONFIG_PATH", DEFAULT_CONFIG_PATH)
        self.values: dict = self.load_config()

    @staticmethod
    def instance():
        if not Config.__instance:
            Config.__instance = Config()
        return Config.__instance

    def load_config(self):
        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def all(self) -> dict:
        return self.values

    def get(self, key):
        return self.values.get(key, {})
