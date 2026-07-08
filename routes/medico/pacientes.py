from flask import Blueprint, render_template, request, redirect, url_for, session
from database.conexion import get_connection

pacientes_medico = Blueprint(
    "pacientes_medico",
    __name__
)

# LISTAR PACIENTES

@pacientes_medico.route("/medico/pacientes")
def listar_pacientes():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") != "medico":
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
            f.numero_carpeta

        FROM pacientes p

        INNER JOIN familias f

            ON p.id_familia=f.id_familia

        WHERE p.activo=TRUE

        ORDER BY

            p.apellidos,
            p.nombres

    """)

    pacientes = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "medico/pacientes/listar.html",
        pacientes=pacientes
    )

# BUSCAR PACIENTE

@pacientes_medico.route("/medico/pacientes/buscar")
def buscar_paciente():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") != "medico":
        return redirect(url_for("auth.login"))

    buscar = request.args.get("buscar","")

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
            f.numero_carpeta

        FROM pacientes p

        INNER JOIN familias f

            ON p.id_familia=f.id_familia

        WHERE

            LOWER(p.nombres) LIKE LOWER(%s)

            OR LOWER(p.apellidos) LIKE LOWER(%s)

            OR p.ci LIKE %s

        ORDER BY

            p.apellidos,
            p.nombres

    """,

    (

        f"%{buscar}%",

        f"%{buscar}%",

        f"%{buscar}%"

    ))

    pacientes = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(

        "medico/pacientes/listar.html",

        pacientes=pacientes

    )

# VER HISTORIAL DEL PACIENTE

@pacientes_medico.route("/medico/pacientes/<int:id_paciente>")
def ver_paciente(id_paciente):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") != "medico":
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    # DATOS DEL PACIENTE

    cur.execute("""

        SELECT

            p.id_paciente,
            p.nombres,
            p.apellidos,
            p.ci,
            p.fecha_nacimiento,
            p.genero,
            f.numero_carpeta

        FROM pacientes p

        INNER JOIN familias f

            ON p.id_familia = f.id_familia

        WHERE p.id_paciente=%s

    """,(id_paciente,))

    paciente = cur.fetchone()

    # HISTORIAL DE CONSULTAS

    cur.execute("""

        SELECT

            c.id_consulta,

            c.fecha_consulta,

            u.nombres_completos,

            c.diagnostico

        FROM consultas c

        INNER JOIN usuarios u

            ON c.id_medico = u.id_usuario

        WHERE c.id_paciente=%s

        ORDER BY c.fecha_consulta DESC

    """,(id_paciente,))

    consultas = cur.fetchall()


    cur.close()
    conn.close()

    return render_template(

        "medico/pacientes/ver.html",

        paciente=paciente,

        consultas=consultas

    )