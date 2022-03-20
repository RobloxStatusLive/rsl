# Copyright 2022 iiPython

# Modules
import json
from rsl import app
from flask import render_template

# Routes
@app.route("/")
def route_index() -> None:
    data = json.loads(open("db/data.json", "r").read())
    slow = [s for n, s in data.items() if s["guess"][0] == "slow"]
    down = [s for n, s in data.items() if s["guess"][0] == "down"]
    return render_template(
        "index.html",
        data = sorted([d for n, d in data.items()], key = lambda d: d["name"]),
        status = ("down", "red") if len(down) > 3 else (("partially down", "yellow") if len(slow) > 3 else ("online", "green"))
    ), 200
