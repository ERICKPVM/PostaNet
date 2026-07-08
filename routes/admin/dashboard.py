from flask import Blueprint, render_template, session, redirect, url_for

dashboard_admin = Blueprint(
    "dashboard_admin",
    __name__
)

@dashboard_admin.route("/admin/dashboard")
def dashboard():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") != "administrador":
        return redirect(url_for("auth.login"))

    return render_template("admin/dashboard.html")