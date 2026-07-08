from flask import Blueprint, render_template, request, redirect, url_for, session
from database.conexion import get_connection

consultas = Blueprint(
    "consultas",
    __name__
)

# FORMULARIO NUEVA CONSULTA

@consultas.route("/medico/consultas/nueva/<int:id_paciente>")
def nueva_consulta(id_paciente):

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

        WHERE p.id_paciente=%s

    """,(id_paciente,))

    paciente = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(

        "medico/consultas/nueva.html",

        paciente=paciente

    )

# GUARDAR CONSULTA

@consultas.route("/medico/consultas/guardar", methods=["POST"])
def guardar_consulta():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    id_paciente = request.form["id_paciente"]

    motivo = request.form["motivo"]

    signos = request.form["signos"]

    diagnostico = request.form["diagnostico"]

    tratamiento = request.form["tratamiento"]

    observaciones = request.form["observaciones"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT id_usuario

        FROM usuarios

        WHERE nombre_usuario=%s

    """,(session["usuario"],))

    id_medico = cur.fetchone()[0]

    cur.execute("""

        INSERT INTO consultas
        (

            id_paciente,

            id_medico,

            motivo_consulta,

            signos_vitales,

            diagnostico,

            tratamiento,

            observaciones

        )

        VALUES
        (

            %s,

            %s,

            %s,

            %s,

            %s,

            %s,

            %s

        )

    """,

    (

        id_paciente,

        id_medico,

        motivo,

        signos,

        diagnostico,

        tratamiento,

        observaciones

    ))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(

        url_for(

            "pacientes_medico.ver_paciente",

            id_paciente=id_paciente

        )

    )

# VER CONSULTA

@consultas.route("/medico/consultas/<int:id_consulta>")
def ver_consulta(id_consulta):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    if session.get("rol") != "medico":
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            c.id_consulta,

            c.fecha_consulta,

            p.nombres,

            p.apellidos,

            p.ci,

            u.nombres_completos,

            c.motivo_consulta,

            c.signos_vitales,

            c.diagnostico,

            c.tratamiento,

            c.observaciones

        FROM consultas c

        INNER JOIN pacientes p

            ON c.id_paciente = p.id_paciente

        INNER JOIN usuarios u

            ON c.id_medico = u.id_usuario

        WHERE c.id_consulta = %s

    """,(id_consulta,))

    consulta = cur.fetchone()

    cur.close()
    conn.close()

    return render_template(

        "medico/consultas/ver.html",

        consulta=consulta

    )
