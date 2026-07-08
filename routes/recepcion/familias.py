from flask import Blueprint, render_template, request, redirect, url_for, session
from database.conexion import get_connection

familias = Blueprint("familias", __name__)

# LISTAR CARPETAS

@familias.route("/recepcion/familias")
def listar_familias():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            f.id_familia,
            f.numero_carpeta,

            COALESCE(

                (
                    SELECT
                        p.nombres || ' ' || p.apellidos

                    FROM pacientes p

                    WHERE p.id_familia = f.id_familia

                    ORDER BY p.id_paciente

                    LIMIT 1
                ),

                'Sin pacientes'

            ) AS paciente_principal,

            f.direccion,

            z.nombre_zona,

            f.ubicacion_fisica,

            f.estado_carpeta

        FROM familias f

        INNER JOIN zonas z

            ON f.id_zona = z.id_zona

        ORDER BY f.numero_carpeta

    """)

    familias_db = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "recepcion/familias/listar.html",
        familias=familias_db
    )

# FORMULARIO NUEVA CARPETA

@familias.route("/recepcion/familias/nueva")
def nueva_familia():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            id_zona,
            nombre_zona

        FROM zonas

        ORDER BY nombre_zona

    """)

    zonas = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "recepcion/familias/registrar.html",
        zonas=zonas
    )
    
# GUARDAR CARPETA

@familias.route("/recepcion/familias/guardar", methods=["POST"])
def guardar_familia():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    direccion = request.form["direccion"]
    id_zona = request.form["id_zona"]
    ubicacion_fisica = request.form["ubicacion_fisica"]

    conn = get_connection()
    cur = conn.cursor()

    # Obtener el siguiente id de la secuencia
    cur.execute("""
        SELECT nextval('public.familias_id_familia_seq')
    """)

    id_familia = cur.fetchone()[0]

    # Generar el número de carpeta
    numero_carpeta = f"CF-{id_familia:06d}"

    # Insertar la carpeta
    cur.execute("""

        INSERT INTO familias
        (
            id_familia,
            numero_carpeta,
            direccion,
            id_zona,
            ubicacion_fisica
        )

        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s
        )

    """,
    (
        id_familia,
        numero_carpeta,
        direccion,
        id_zona,
        ubicacion_fisica
    ))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("familias.listar_familias"))

# FORMULARIO EDITAR CARPETA

@familias.route("/recepcion/familias/editar/<int:id_familia>")
def editar_familia(id_familia):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT
            id_familia,
            numero_carpeta,
            direccion,
            id_zona,
            ubicacion_fisica,
            estado_carpeta

        FROM familias

        WHERE id_familia=%s

    """,(id_familia,))

    familia = cur.fetchone()

    cur.execute("""

        SELECT
            id_zona,
            nombre_zona

        FROM zonas

        ORDER BY nombre_zona

    """)

    zonas = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "recepcion/familias/editar.html",
        familia=familia,
        zonas=zonas
    )

# ACTUALIZAR CARPETA

@familias.route("/recepcion/familias/actualizar", methods=["POST"])
def actualizar_familia():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    id_familia = request.form["id_familia"]
    numero_carpeta = request.form["numero_carpeta"]
    direccion = request.form["direccion"]
    id_zona = request.form["id_zona"]
    ubicacion_fisica = request.form["ubicacion_fisica"]
    estado = request.form["estado"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        UPDATE familias

        SET

            numero_carpeta=%s,
            direccion=%s,
            id_zona=%s,
            ubicacion_fisica=%s,
            estado_carpeta=%s

        WHERE id_familia=%s

    """,
    (
        numero_carpeta,
        direccion,
        id_zona,
        ubicacion_fisica,
        estado,
        id_familia
    ))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(url_for("familias.listar_familias"))

# BUSCAR CARPETA

@familias.route("/recepcion/familias/buscar", methods=["GET"])
def buscar_familia():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    buscar = request.args.get("buscar", "").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT DISTINCT

            f.id_familia,
            f.numero_carpeta,
            f.direccion,
            z.nombre_zona,
            f.ubicacion_fisica,
            f.estado_carpeta

        FROM familias f

        INNER JOIN zonas z
            ON f.id_zona = z.id_zona

        LEFT JOIN pacientes p
            ON p.id_familia = f.id_familia

        WHERE

            LOWER(f.numero_carpeta) LIKE LOWER(%s)

            OR LOWER(COALESCE(p.nombres,'')) LIKE LOWER(%s)

            OR LOWER(COALESCE(p.apellidos,'')) LIKE LOWER(%s)

            OR COALESCE(p.ci,'') LIKE %s

        ORDER BY f.numero_carpeta

    """,
    (
        f"%{buscar}%",
        f"%{buscar}%",
        f"%{buscar}%",
        f"%{buscar}%"
    ))

    familias_db = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "recepcion/familias/listar.html",
        familias=familias_db
    )

# VER CARPETA FAMILIAR

@familias.route("/recepcion/familias/<int:id_familia>")
def ver_familia(id_familia):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    conn = get_connection()
    cur = conn.cursor()

    # DATOS DE LA CARPETA

    cur.execute("""

        SELECT

            f.id_familia,
            f.numero_carpeta,
            f.direccion,
            z.nombre_zona,
            f.ubicacion_fisica,
            f.estado_carpeta

        FROM familias f

        INNER JOIN zonas z

            ON f.id_zona = z.id_zona

        WHERE f.id_familia=%s

    """,(id_familia,))

    familia = cur.fetchone()

    # PACIENTES DE LA CARPETA

    cur.execute("""

        SELECT

            id_paciente,
            nombres,
            apellidos,
            ci,
            fecha_nacimiento,
            genero,
            activo

        FROM pacientes

        WHERE id_familia=%s

        ORDER BY id_paciente

    """,(id_familia,))

    pacientes = cur.fetchall()

    # DOCUMENTOS DE LA CARPETA

    cur.execute("""

        SELECT

            id_documento,
            tipo_documento,
            ruta_archivo,
            fecha_subida

        FROM documentos

        WHERE id_familia=%s

        ORDER BY fecha_subida DESC

    """,(id_familia,))

    documentos = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "recepcion/familias/ver.html",
        familia=familia,
        pacientes=pacientes,
        documentos=documentos
    )