# Copyright 2022 iiPython

# Modules
from rsl import app, rpath
from flask import render_template, send_from_directory

# Routes
@app.route("/", methods = ["GET"])
def route_index() -> None:
    data = app.db.get_current()
    return render_template(
        "index.html",
        data = [data[i:i + 4] for i in range(0, len(data), 4)],
        status = app.db.guess_status(data)
    ), 200

@app.route("/s/<path:path>", methods = ["GET"])
def route_static_file(path: str) -> None:
    return send_from_directory(rpath("src/static"), path, conditional = True)

# Error handlers
@app.errorhandler(400)
def route_err_400(e) -> None:
    return render_template("errors/400.html"), 400

@app.errorhandler(404)
def route_err_404(e) -> None:
    return render_template("errors/404.html"), 404

@app.errorhandler(500)
def route_error_500(e) -> None:
    return render_template("errors/500.html"), 500
