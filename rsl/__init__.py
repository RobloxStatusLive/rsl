# Copyright 2022 iiPython

# Modules
import os
from flask import Flask

# Initialization
def rpath(path: str) -> str:
    return os.path.join(os.path.dirname(__file__), path)

app = Flask(
    "Roblox Status Live",
    template_folder = rpath("src/templates")
)
app.version = "1.1"

# Jinja env
@app.context_processor
def add_globals() -> dict:
    return {"app": app}

# Start service launcher
if "RSLSTARTED" not in os.environ:
    os.environ["RSLSTARTED"] = "1"

    from .services import ServiceTracker
    ServiceTracker()

# Load routes
from .routes import (public, api)
