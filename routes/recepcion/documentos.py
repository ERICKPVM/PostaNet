from flask import Blueprint, request, redirect, url_for, session
from database.conexion import get_connection
import os
import uuid

documentos = Blueprint("documentos", __name__)

EXTENSIONES = {"pdf", "png", "jpg", "jpeg"}


# VALIDAR EXTENSIÓN

def archivo_permitido(nombre):

    return (
        "." in nombre and
        nombre.rsplit(".", 1)[1].lower() in EXTENSIONES
    )

# SUBIR DOCUMENTO

@documentos.route(
    "/recepcion/documentos/subir",
    methods=["POST"]
)
def subir_documento():

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    archivo = request.files["archivo"]
    tipo_documento = request.form["tipo_documento"]
    id_familia = request.form["id_familia"]

    if archivo.filename == "":
        return redirect(
            url_for(
                "familias.ver_familia",
                id_familia=id_familia
            )
        )

    if archivo and archivo_permitido(archivo.filename):

        extension = archivo.filename.rsplit(".", 1)[1].lower()

        nombre = str(uuid.uuid4()) + "." + extension

        ruta = os.path.join(
            "static",
            "uploads",
            "documentos",
            nombre
        )

        conn = get_connection()
        cur = conn.cursor()

        # VERIFICAR SI YA EXISTE

        cur.execute("""

            SELECT

                id_documento,
                ruta_archivo

            FROM documentos

            WHERE

                id_familia=%s

                AND tipo_documento=%s

        """,
        (
            id_familia,
            tipo_documento
        ))

        documento = cur.fetchone()

        if documento:

            if os.path.exists(documento[1]):
                os.remove(documento[1])

            cur.execute("""

                DELETE FROM documentos

                WHERE id_documento=%s

            """,(documento[0],))

        # GUARDAR ARCHIVO

        archivo.save(ruta)

        # INSERTAR EN BD

        cur.execute("""

            INSERT INTO documentos
            (
                id_familia,
                tipo_documento,
                ruta_archivo,
                subido_por
            )

            VALUES
            (
                %s,
                %s,
                %s,
                (
                    SELECT id_usuario

                    FROM usuarios

                    WHERE nombre_usuario=%s
                )
            )

        """,
        (
            id_familia,
            tipo_documento,
            ruta,
            session["usuario"]
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

# ELIMINAR DOCUMENTO

@documentos.route("/recepcion/documentos/eliminar/<int:id_documento>")
def eliminar_documento(id_documento):

    if "usuario" not in session:
        return redirect(url_for("auth.login"))

    id_familia = request.args.get("id_familia")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""

        SELECT

            ruta_archivo

        FROM documentos

        WHERE id_documento=%s

    """,(id_documento,))

    documento = cur.fetchone()

    if documento:

        if os.path.exists(documento[0]):
            os.remove(documento[0])

    cur.execute("""

        DELETE FROM documentos

        WHERE id_documento=%s

    """,(id_documento,))

    conn.commit()

    cur.close()
    conn.close()

    return redirect(
        url_for(
            "familias.ver_familia",
            id_familia=id_familia
        )
    )