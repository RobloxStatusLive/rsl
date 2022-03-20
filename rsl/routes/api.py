# Copyright 2022 iiPython

# Modules
import json
from rsl import app
from flask import jsonify

# Routes
@app.route("/api/status")
def route_api_status() -> None:
    data = json.loads(open("db/current.json", "r").read())
    slow = [s for n, s in data.items() if s["guess"][0] == "slow"]
    down = [s for n, s in data.items() if s["guess"][0] == "down"]
    return jsonify(
        services =  sorted([d for n, d in data.items()], key = lambda d: d["name"]),
        status = ("down", "red") if len(down) > 3 else (("partially down", "yellow") if len(slow) > 3 else ("online", "green"))
    ), 200
