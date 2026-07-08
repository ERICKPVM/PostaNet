from flask import Blueprint, render_template, request, session, redirect, url_for
from database.conexion import get_connection

usuarios = Blueprint("usuarios", __name__)


# LISTAR USUARIOS

@usuarios.route("/admin/usuarios")
def listar_usuarios():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_usuario,
            nombre_usuario,
            nombres_completos,
            rol,
            activo
        FROM usuarios
        ORDER BY id_usuario
    """)

    usuarios_db = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "admin/usuarios/listar.html",
        usuarios=usuarios_db
    )

# FORMULARIO NUEVO USUARIO

@usuarios.route("/admin/usuarios/nuevo")
def nuevo_usuario():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    return render_template("admin/usuarios/registrar.html")


# GUARDAR USUARIO

@usuarios.route("/admin/usuarios/guardar", methods=["POST"])
def guardar_usuario():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    nombre_usuario = request.form["nombre_usuario"]
    password = request.form["password"]
    nombre_completo = request.form["nombre_completo"]
    rol = request.form["rol"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id_usuario FROM usuarios WHERE nombre_usuario=%s",
        (nombre_usuario,)
    )

    existe = cur.fetchone()

    if existe:

        cur.close()
        conn.close()

        return render_template(
            "admin/usuarios/registrar.html",
            error="Ese nombre de usuario ya existe."
        )

    cur.execute("""
        INSERT INTO usuarios
        (
            nombre_usuario,
            password_hash,
            nombres_completos,
            rol
        )
        VALUES(%s,%s,%s,%s)
    """,
    (
        nombre_usuario,
        password,
        nombre_completo,
        rol
    ))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("usuarios.listar_usuarios"))


# EDITAR

@usuarios.route("/admin/usuarios/editar/<int:id_usuario>")
def editar_usuario(id_usuario):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_usuario,
            nombre_usuario,
            nombres_completos,
            rol
        FROM usuarios
        WHERE id_usuario=%s
    """,(id_usuario,))

    usuario = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(
        "admin/usuarios/editar.html",
        usuario=usuario
    )

# ACTUALIZAR

@usuarios.route("/admin/usuarios/actualizar", methods=["POST"])
def actualizar_usuario():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    id_usuario = request.form["id_usuario"]
    nombre_usuario = request.form["nombre_usuario"]
    nombre_completo = request.form["nombre_completo"]
    rol = request.form["rol"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE usuarios
        SET
            nombre_usuario=%s,
            nombres_completos=%s,
            rol=%s
        WHERE id_usuario=%s
    """,
    (
        nombre_usuario,
        nombre_completo,
        rol,
        id_usuario
    ))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("usuarios.listar_usuarios"))

# DESACTIVAR

@usuarios.route("/admin/usuarios/desactivar/<int:id_usuario>")
def desactivar_usuario(id_usuario):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE usuarios
        SET activo=FALSE
        WHERE id_usuario=%s
    """,(id_usuario,))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("usuarios.listar_usuarios"))

# ACTIVAR

@usuarios.route("/admin/usuarios/activar/<int:id_usuario>")
def activar_usuario(id_usuario):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE usuarios
        SET activo=TRUE
        WHERE id_usuario=%s
    """,(id_usuario,))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("usuarios.listar_usuarios"))