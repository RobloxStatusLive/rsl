# Copyright 2022 iiPython

# Modules
from rsl import app
from flask import abort, jsonify, request, redirect, render_template

# Routes
@app.route("/api")
def route_api_doc_redirect() -> None:
    return redirect("/api/docs")

@app.route("/api/docs")
def route_api_docs() -> None:
    return render_template("api.html"), 200

@app.route("/api/status")
def route_api_status() -> None:
    data = app.db.get_current()
    return jsonify(
        services =  data,
        status = app.db.guess_status(data)
    ), 200

@app.route("/api/historical")
def route_api_historical() -> None:
    try:
        service_data = app.db.get_service_data(request.args.get("id"))
        if not service_data:
            return abort(404)

    except Exception:
        return abort(404)

    return jsonify(
        name = service_data[0],
        data = service_data[1],
        uptime = service_data[2]
    ), 200
