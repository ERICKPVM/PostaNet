from flask import Blueprint, render_template, request, redirect, url_for, session
from database.conexion import get_connection

pacientes = Blueprint("pacientes", __name__)


# =====================================
# LISTAR PACIENTES
# =====================================

@pacientes.route("/recepcion/pacientes")
def listar_pacientes():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            p.id_paciente,
            p.nombres,
            p.apellidos,
            p.ci,
            p.fecha_nacimiento,
            p.genero,
            f.numero_carpeta,
            p.activo

        FROM pacientes p

        INNER JOIN familias f

            ON p.id_familia = f.id_familia

        ORDER BY p.apellidos, p.nombres

    """)

    pacientes_db = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "recepcion/pacientes/listar.html",
        pacientes=pacientes_db
    )


# =====================================
# FORMULARIO NUEVO PACIENTE
# =====================================

@pacientes.route("/recepcion/pacientes/nuevo")
def nuevo_paciente():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    id_familia = request.args.get("id_familia")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            id_familia,
            numero_carpeta
        FROM familias
        ORDER BY numero_carpeta
    """)

    familias = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "recepcion/pacientes/registrar.html",
        familias=familias,
        id_familia=id_familia
    )
# =====================================
# GUARDAR PACIENTE
# =====================================

@pacientes.route("/recepcion/pacientes/guardar", methods=["POST"])
def guardar_paciente():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    ci = request.form["ci"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    genero = request.form["genero"]
    id_familia = request.form["id_familia"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        INSERT INTO pacientes
        (
            nombres,
            apellidos,
            ci,
            fecha_nacimiento,
            genero,
            id_familia
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )

    """,
    (
        nombres,
        apellidos,
        ci,
        fecha_nacimiento,
        genero,
        id_familia
    ))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(
        url_for(
            "familias.ver_familia",
            id_familia=id_familia
        )
    )
# =====================================
# FORMULARIO EDITAR PACIENTE
# =====================================

@pacientes.route("/recepcion/pacientes/editar/<int:id_paciente>")
def editar_paciente(id_paciente):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            id_paciente,
            nombres,
            apellidos,
            ci,
            fecha_nacimiento,
            genero,
            id_familia

        FROM pacientes

        WHERE id_paciente=%s

    """,(id_paciente,))

    paciente = cur.fetchone()

    cur.execute("""

        SELECT

            id_familia,
            numero_carpeta

        FROM familias

        ORDER BY numero_carpeta

    """)

    familias = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "recepcion/pacientes/editar.html",
        paciente=paciente,
        familias=familias
    )


# =====================================
# ACTUALIZAR PACIENTE
# =====================================

@pacientes.route("/recepcion/pacientes/actualizar", methods=["POST"])
def actualizar_paciente():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    id_paciente = request.form["id_paciente"]
    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    ci = request.form["ci"]
    fecha_nacimiento = request.form["fecha_nacimiento"]
    genero = request.form["genero"]
    id_familia = request.form["id_familia"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        UPDATE pacientes

        SET

            nombres=%s,
            apellidos=%s,
            ci=%s,
            fecha_nacimiento=%s,
            genero=%s,
            id_familia=%s

        WHERE id_paciente=%s

    """,
    (
        nombres,
        apellidos,
        ci,
        fecha_nacimiento,
        genero,
        id_familia,
        id_paciente
    ))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(
        url_for(
            "familias.ver_familia",
            id_familia=id_familia
        )
    )
# =====================================
# BUSCAR PACIENTE
# =====================================

@pacientes.route("/recepcion/pacientes/buscar")
def buscar_paciente():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    buscar = request.args.get("buscar", "")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            p.id_paciente,
            p.nombres,
            p.apellidos,
            p.ci,
            p.fecha_nacimiento,
            p.genero,
            f.numero_carpeta,
            p.activo

        FROM pacientes p

        INNER JOIN familias f

            ON p.id_familia=f.id_familia

        WHERE

            LOWER(p.nombres) LIKE LOWER(%s)

            OR LOWER(p.apellidos) LIKE LOWER(%s)

            OR p.ci LIKE %s

        ORDER BY p.apellidos,p.nombres

    """,
    (
        f"%{buscar}%",
        f"%{buscar}%",
        f"%{buscar}%"
    ))

    pacientes_db = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "recepcion/pacientes/listar.html",
        pacientes=pacientes_db
    )
    # =====================================
# DESACTIVAR PACIENTE
# =====================================

@pacientes.route("/recepcion/pacientes/desactivar/<int:id_paciente>")
def desactivar_paciente(id_paciente):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        UPDATE pacientes

        SET activo = FALSE

        WHERE id_paciente = %s

    """, (id_paciente,))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("pacientes.listar_pacientes"))


# =====================================
# ACTIVAR PACIENTE
# =====================================

@pacientes.route("/recepcion/pacientes/activar/<int:id_paciente>")
def activar_paciente(id_paciente):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        UPDATE pacientes

        SET activo = TRUE

        WHERE id_paciente = %s

    """, (id_paciente,))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("pacientes.listar_pacientes"))