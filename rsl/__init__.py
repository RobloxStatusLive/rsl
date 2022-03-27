# Copyright 2022 iiPython

# Modules
import os
import sys
from flask import Flask

from .reader import DBLoader

# Initialization
def rpath(path: str) -> str:
    return os.path.join(os.path.dirname(__file__), path)

sys.modules["flask.cli"].show_server_banner = lambda *x: None

# Load app
app = Flask(
    "Roblox Status Live",
    template_folder = rpath("src/templates")
)
app.version = "1.2"
app.secret_key = os.environ.get("SECRET", "default")
app.admin_alert = ""

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
