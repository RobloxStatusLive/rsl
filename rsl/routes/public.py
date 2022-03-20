# Copyright 2022 iiPython

# Modules
import json
from rsl import app, rpath
from flask import render_template, send_from_directory

# Routes
@app.route("/")
def route_index() -> None:
    data = json.loads(open("db/current.json", "r").read())
    slow = [s for n, s in data.items() if s["guess"][0] == "slow"]
    down = [s for n, s in data.items() if s["guess"][0] == "down"]
    return render_template(
        "index.html",
        data = sorted([d for n, d in data.items()], key = lambda d: d["name"]),
        status = ("down", "red") if len(down) > 3 else (("partially down", "yellow") if len(slow) > 3 else ("online", "green"))
    ), 200

@app.route("/s/<path:path>")
def route_static_file(path: str) -> None:
    return send_from_directory(rpath("src/static"), path, conditional = True)
