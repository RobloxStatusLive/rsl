# Copyright 2022 iiPython

# Modules
import json
from rsl import app
from flask import render_template

# Routes
@app.route("/")
def route_index() -> None:
    data = json.loads(open("db/data.json", "r").read())
    down = [s for n, s in data.items() if s["guess"][0] in ["slow", "down"]]
    return render_template(
        "index.html",
        data = data,
        status = ("online", "green") if not down else (("partially down", "yellow") if len(down) < 3 else ("down", "red"))
    ), 200
