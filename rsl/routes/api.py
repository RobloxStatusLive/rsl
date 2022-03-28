# Copyright 2022 iiPython

# Modules
from rsl import app
from flask import abort, jsonify, request, redirect, render_template

# Routes
@app.route("/api", methods = ["GET"])
def route_api_doc_redirect() -> None:
    return redirect("/api/docs")

@app.route("/api/docs", methods = ["GET"])
def route_api_docs() -> None:
    return render_template("api.html"), 200

@app.route("/api/status", methods = ["GET"])
def route_api_status() -> None:
    data = app.db.get_current()
    return jsonify(
        services =  data,
        status = app.db.guess_status(data)
    ), 200

@app.route("/api/historical", methods = ["GET"])
def route_api_historical() -> None:
    service_id, date = request.args.get("id"), request.args.get("date")
    try:
        service_data = app.db.get_service_data(service_id, **{"date": date} if date else {})
        if not service_data:
            return abort(400)

    except Exception:
        return abort(400)

    return jsonify(
        name = service_data[0],
        data = service_data[1],
        uptime = service_data[2]
    ), 200
