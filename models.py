import pymysql


# =====================================================
# INICIALIZAR BASE DE DATOS DESDE ARCHIVO SQL
# =====================================================

def init_db():
    # conexión sin base de datos (para poder crearla)
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="TU_PASSWORD",
        autocommit=True
    )

    cursor = conn.cursor()

    # =================================================
    # LEER Y EJECUTAR ARCHIVO SQL
    # =================================================
    with open("database/database.sql", "r", encoding="utf-8") as file:
        sql_script = file.read()

    # separar sentencias
    statements = sql_script.split(";")

    for statement in statements:
        statement = statement.strip()
        if statement:
            cursor.execute(statement)

    cursor.close()
    conn.close()