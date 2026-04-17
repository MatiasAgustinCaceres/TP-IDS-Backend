import pymysql

def get_connection(database=None):
    return pymysql.connect(
        host="localhost",
        user="root",
        password="TU_PASSWORD",
        database=database,
        autocommit=True
    )


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. crear DB si no existe
    cursor.execute("CREATE DATABASE IF NOT EXISTS tp_ids")

    # 2. conectar a la DB
    conn.select_db("tp_ids")

    # 3. leer archivo SQL
    with open("database/database.sql", "r", encoding="utf-8") as file:
        sql_script = file.read()

    # 4. ejecutar statements
    statements = sql_script.split(";")

    for stmt in statements:
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt)

    cursor.close()
    conn.close()