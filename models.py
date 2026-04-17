import pymysql


def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Hola-15935726840",
        database="tp_ids",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )


# =====================================================
# INICIALIZACIÓN DE BASE DE DATOS
# =====================================================

def init_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="Hola-15935726840",
        autocommit=True
    )

    cursor = conn.cursor()

    with open("database/database.sql", "r", encoding="utf-8") as file:
        sql_script = file.read()

    for statement in sql_script.split(";"):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)

    cursor.close()
    conn.close()


# =====================================================
# GET /partidos
# =====================================================

def get_partidos(filtros, limit, offset):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM partidos WHERE 1=1"
    params = []

    if filtros.get("equipo"):
        query += " AND (equipo_local = %s OR equipo_visitante = %s)"
        params.append(filtros["equipo"])
        params.append(filtros["equipo"])

    if filtros.get("fecha"):
        query += " AND fecha = %s"
        params.append(filtros["fecha"])

    if filtros.get("fase"):
        query += " AND fase = %s"
        params.append(filtros["fase"])

    query += " LIMIT %s OFFSET %s"
    params.append(limit)
    params.append(offset)

    cursor.execute(query, params)
    resultados = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultados
