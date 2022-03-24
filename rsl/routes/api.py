# Copyright 2022 iiPython

# Modules
from rsl import app
from flask import abort, jsonify, request

# Routes
@app.route("/api/status")
def route_api_status() -> None:
    data = app.db.get_current()
    return jsonify(
        services =  data,
        status = app.db.guess_status(data)
    ), 200

@app.route("/api/historical")
def route_api_historical() -> None:
    service_data = app.db.get_service_data(request.args.get("id"))
    if not service_data:
        return abort(400)

    return jsonify(
        name = service_data[0],
        data = service_data[1],
        uptime = service_data[2]
    ), 200
