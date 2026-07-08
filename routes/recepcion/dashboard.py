from flask import Blueprint, render_template, session, redirect, url_for
from database.conexion import get_connection

dashboard_recepcion = Blueprint("dashboard_recepcion", __name__)


@dashboard_recepcion.route("/recepcion/dashboard")
def dashboard():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM familias")
    total_familias = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM pacientes")
    total_pacientes = cur.fetchone()[0]

    cur.close()
    conn.close()

    return render_template(
        "recepcion/dashboard.html",
        total_familias=total_familias,
        total_pacientes=total_pacientes
    )