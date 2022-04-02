# Copyright 2022 iiPython

# Modules
import os
import json
from typing import Any

# Initialization
config_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../config.json"))
global_defaults = {
    "rsl.dataLocation": "./data",
    "logging.useColor": True,
    "logging.dumpToFile": True
}

# Configuration handler
class Configuration(object):
    def __init__(self) -> None:
        self.config = {}
        try:
            with open(config_file, "r") as cf:
                self.config = json.loads(cf.read())

        except Exception:
            pass

    def get(self, key: str, default: Any = None) -> Any:
        if key not in self.config:
            if key in global_defaults or default:
                return global_defaults[key] or default

            print(f"RSL configuration error: key {key} is missing from config file")
            print("Make sure that your config file is not named 'config.ex.json' and is named 'config.json'.")
            return os._exit(1)

        return self.config[key]

config = Configuration()
