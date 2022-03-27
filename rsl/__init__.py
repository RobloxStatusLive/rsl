# Copyright 2022 iiPython

# Modules
import os
import sys
from flask import Flask

from .config import config
from .reader import DBLoader
from ._logging import log

# Initialization
def rpath(path: str) -> str:
    return os.path.join(os.path.dirname(__file__), path)

sys.modules["flask.cli"].show_server_banner = lambda *x: None

# Load app
app = Flask(
    "Roblox Status Live",
    template_folder = rpath("src/templates")
)
app.version = "2.0"
app.secret_key = config.get("rsl.secret")

# Jinja env
@app.context_processor
def add_globals() -> dict:
    return {"app": app}

# Start service launcher
if "RSLSTARTED" not in os.environ:
    os.environ["RSLSTARTED"] = "1"

    from .services import ServiceTracker
    ServiceTracker()

app.db = DBLoader()

# Load routes
from .routes import (public, api, admin)
