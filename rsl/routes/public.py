# Copyright 2022 iiPython

# Modules
from rsl import app, rpath
from flask import render_template, send_from_directory

# Routes
@app.route("/")
def route_index() -> None:
    data = app.db.get_current()
    return render_template(
        "index.html",
        data = data,
        status = app.db.guess_status(data)
    ), 200

@app.route("/s/<path:path>")
def route_static_file(path: str) -> None:
    return send_from_directory(rpath("src/static"), path, conditional = True)
