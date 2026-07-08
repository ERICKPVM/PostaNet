from flask import Blueprint, render_template, request, session, redirect, url_for
from database.conexion import get_connection

zonas = Blueprint("zonas", __name__)

# LISTAR ZONAS

@zonas.route("/admin/zonas")
def listar_zonas():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_zona,
            nombre_zona
        FROM zonas
        ORDER BY id_zona
    """)

    zonas_db = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "admin/zonas/listar.html",
        zonas=zonas_db
    )

# NUEVA ZONA

@zonas.route("/admin/zonas/nueva")
def nueva_zona():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    return render_template("admin/zonas/registrar.html")

# GUARDAR ZONA

@zonas.route("/admin/zonas/guardar", methods=["POST"])
def guardar_zona():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    nombre = request.form["nombre_zona"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO zonas(nombre_zona)
        VALUES(%s)
    """, (nombre,))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("zonas.listar_zonas"))


# EDITAR ZONA

@zonas.route("/admin/zonas/editar/<int:id_zona>")
def editar_zona(id_zona):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_zona,
            nombre_zona
        FROM zonas
        WHERE id_zona=%s
    """, (id_zona,))

    zona = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(
        "admin/zonas/editar.html",
        zona=zona
    )

# ACTUALIZAR ZONA

@zonas.route("/admin/zonas/actualizar", methods=["POST"])
def actualizar_zona():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    id_zona = request.form["id_zona"]
    nombre = request.form["nombre_zona"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE zonas
        SET nombre_zona=%s
        WHERE id_zona=%s
    """,
    (
        nombre,
        id_zona
    ))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("zonas.listar_zonas"))

# ELIMINAR ZONA

@zonas.route("/admin/zonas/eliminar/<int:id_zona>")
def eliminar_zona(id_zona):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM zonas
        WHERE id_zona=%s
    """, (id_zona,))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("zonas.listar_zonas"))