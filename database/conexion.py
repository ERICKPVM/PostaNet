import psycopg2


def get_connection():

    conexion = psycopg2.connect(
        host="localhost",
        database="postanet_db",
        user="postgres",
        password="1234"
    )

    return conexion