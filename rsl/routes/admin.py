# Copyright 2022 iiPython

# Modules
import os
import json
import hashlib
from rsl import app
from flask import session, request, redirect, render_template

# Initialization
admin_db = os.path.join(os.environ["_RSL_DB"], "admin.json")

def load_admin_data() -> dict:
    with open(admin_db, "r") as f:
        return json.loads(f.read())

def dump_admin_data(data: dict) -> None:
    with open(admin_db, "w") as f:
        f.write(json.dumps(data, indent = 4))

def hashpw(password: str) -> str:
    return hashlib.sha512(password.encode("utf-8")).hexdigest()

app.admin_alert = load_admin_data()["message"]

# Handle admin auth
@app.before_request
def handle_req() -> None:
    if "/admin/" in request.base_url and not request.base_url.endswith("/admin/login") and "admin" not in session:
        return redirect("/admin/login")

# Routes
@app.route("/admin")
def route_admin_redir() -> None:
    return redirect("/admin/home")

@app.route("/admin/home")
def route_admin() -> None:
    return render_template("admin/home.html"), 200

@app.route("/admin/login", methods = ["GET", "POST"])
def route_admin_login() -> None:
    if request.method == "GET":
        return render_template("admin/login.html"), 200

    username = request.form.get("username", "")
    password = request.form.get("password", "")

    # Check data
    admin_data = load_admin_data()
    actual_password = admin_data["users"].get(username, None)
    if actual_password == "":
        session["admin"] = username
        return redirect("/admin/changepw")

    elif actual_password != hashpw(password):
        return render_template("admin/login.html", error = "Invalid username or password."), 200

    session["admin"] = username
    return redirect("/admin/home")

@app.route("/admin/changepw", methods = ["GET", "POST"])
def route_admin_changepw() -> None:
    if request.method == "GET":
        return render_template("admin/changepw.html"), 200

    password = request.form.get("password", "")
    if not password.strip():
        return render_template("admin/changepw.html", error = "Invalid password."), 200

    # Change password
    admin_data = load_admin_data()
    admin_data["users"][session["admin"]] = hashpw(password)
    dump_admin_data(admin_data)

    # Redirect
    return redirect("/admin/home")

@app.route("/admin/postalert", methods = ["GET"])
def route_admin_postalert() -> None:
    admin_data = load_admin_data()
    admin_data["message"] = request.args.get("alert", "")
    app.admin_alert = admin_data["message"]
    dump_admin_data(admin_data)
    return "200 OK", 200

@app.route("/admin/logout")
def route_admin_logout() -> None:
    if "admin" in session:
        del session["admin"]

    return redirect("/")
