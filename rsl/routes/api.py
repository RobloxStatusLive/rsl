# Copyright 2022 iiPython

# Modules
import io
import json
import tarfile
from rsl import app
from flask import abort, jsonify, request, redirect, send_file, render_template

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

@app.route("/api/download", methods = ["GET"])
def route_api_download() -> None:
    try:
        date = request.args.get("date")
        service_data = app.db.get_date_all(date, loopback = False)

    except Exception:
        return abort(400)

    # Compress and send off to client
    fh, data = io.BytesIO(), json.dumps(service_data)
    with tarfile.open(fileobj = fh, mode = "w:gz") as tar:
        info = tarfile.TarInfo(f"{date}.json")
        info.size = len(data)
        tar.addfile(info, io.BytesIO(initial_bytes = data.encode()))

    fh.seek(0)
    return send_file(
        fh,
        mimetype = "application/gzip",
        as_attachment = True,
        attachment_filename = f"{date}.tgz"
    )
