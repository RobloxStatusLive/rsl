# Copyright 2022 iiPython

# Modules
import os
import logging
from flask import Flask

from .reader import DBLoader

# Initialization
log = logging.getLogger("werkzeug")  # No need for request logs
log.setLevel(logging.ERROR)

def rpath(path: str) -> str:
    return os.path.join(os.path.dirname(__file__), path)

app = Flask(
    "Roblox Status Live",
    template_folder = rpath("src/templates")
)
app.version = "1.2"
app.secret_key = os.environ.get("SECRET", "default")

# Extra data
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
