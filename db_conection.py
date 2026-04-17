import pymysql


# =====================================================
# CONEXIÓN
# =====================================================

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
# INIT DB
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