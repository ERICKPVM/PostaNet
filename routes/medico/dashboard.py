from flask import Blueprint, render_template, session, redirect, url_for
from database.conexion import get_connection

dashboard_medico = Blueprint(
    "dashboard_medico",
    __name__
)
@dashboard_medico.route("/medico/dashboard")
def dashboard():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") != "medico":
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()
    # Total pacientes
    cur.execute("""

        SELECT COUNT(*)
        FROM pacientes
        WHERE activo = TRUE
    """)
    total_pacientes = cur.fetchone()[0]

    # Total consultas
    cur.execute("""

        SELECT COUNT(*)
        FROM consultas
    """)
    total_consultas = cur.fetchone()[0]

    # Consultas del día
    cur.execute("""

        SELECT COUNT(*)
        FROM consultas
        WHERE DATE(fecha_consulta)=CURRENT_DATE

    """)
    consultas_hoy = cur.fetchone()[0]

    cur.close()
    conn.close()

    return render_template(
        "medico/dashboard.html",
        total_pacientes=total_pacientes,
        total_consultas=total_consultas,
        consultas_hoy=consultas_hoy
    )