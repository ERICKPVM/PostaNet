from flask import Blueprint, render_template, request, session, redirect, url_for
from database.conexion import get_connection

auth = Blueprint("auth", __name__)

# LOGIN

@auth.route("/", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    usuario = request.form["usuario"]
    password = request.form["password"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            nombre_usuario,
            password_hash,
            rol,
            activo
        FROM usuarios
        WHERE nombre_usuario=%s
    """,(usuario,))

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:

        return "<h2>Usuario o contraseña incorrectos</h2>"

    db_user, db_pass, rol, activo = user

    if not activo:

        return "<h2>Usuario desactivado</h2>"

    if password != db_pass:

        return "<h2>Usuario o contraseña incorrectos</h2>"

    session["usuario"] = db_user
    session["rol"] = rol

    if rol == "administrador":

        return redirect(url_for("dashboard_admin.dashboard"))

    elif rol == "recepcionista":

        return redirect(url_for("dashboard_recepcion.dashboard"))

    elif rol == "medico":

        return redirect(
            url_for("dashboard_medico.dashboard")
        )

    return redirect(url_for("login"))

# LOGOUT
@auth.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("auth.login"))