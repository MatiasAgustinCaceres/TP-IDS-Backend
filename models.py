from db_conection import get_connection


# =====================================================
# LISTAR PARTIDOS
# =====================================================

def get_partidos(filtros, limit, offset):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM partidos WHERE 1=1"
    params = []

    if filtros.get("equipo"):
        query += " AND (equipo_local = %s OR equipo_visitante = %s)"
        params.extend([filtros["equipo"], filtros["equipo"]])

    if filtros.get("fecha"):
        query += " AND fecha = %s"
        params.append(filtros["fecha"])

    if filtros.get("fase"):
        query += " AND fase = %s"
        params.append(filtros["fase"])

    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cursor.execute(query, params)
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


# =====================================================
# VERIFICAR DUPLICADO
# =====================================================

def get_partido_existente(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM partidos
        WHERE equipo_local = %s
        AND equipo_visitante = %s
        AND fecha = %s
    """, (
        data["equipo_local"],
        data["equipo_visitante"],
        data["fecha"]
    ))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


# =====================================================
# CREATE PARTIDO
# =====================================================

def create_partido(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO partidos (
            equipo_local,
            equipo_visitante,
            estadio,
            ciudad,
            fecha,
            fase
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["equipo_local"],
        data["equipo_visitante"],
        data.get("estadio"),
        data.get("ciudad"),
        data["fecha"],
        data["fase"]
    ))

    cursor.close()
    conn.close()


# =====================================================
# GET BY ID
# =====================================================

def get_partido_by_id(partido_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM partidos WHERE id = %s", (partido_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


# =====================================================
# PUT (REEMPLAZO TOTAL)
# =====================================================

def replace_partido(partido_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE partidos
        SET equipo_local=%s,
            equipo_visitante=%s,
            estadio=%s,
            ciudad=%s,
            fecha=%s,
            fase=%s
        WHERE id=%s
    """, (
        data["equipo_local"],
        data["equipo_visitante"],
        data.get("estadio"),
        data.get("ciudad"),
        data["fecha"],
        data["fase"],
        partido_id
    ))

    cursor.close()
    conn.close()


# =====================================================
# PATCH (PARCIAL)
# =====================================================

def patch_partido(partido_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    fields = []
    values = []

    for key in ["equipo_local", "equipo_visitante", "estadio", "ciudad", "fecha", "fase"]:
        if key in data:
            fields.append(f"{key} = %s")
            values.append(data[key])

    values.append(partido_id)

    query = f"UPDATE partidos SET {', '.join(fields)} WHERE id = %s"

    cursor.execute(query, values)

    cursor.close()
    conn.close()


# =====================================================
# DELETE
# =====================================================

def delete_partido(partido_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM partidos WHERE id = %s", (partido_id,))

    cursor.close()
    conn.close()


# =====================================================
# RESULTADO PARTIDO
# =====================================================

def update_resultado(partido_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE partidos
        SET goles_local = %s,
            goles_visitante = %s
        WHERE id = %s
    """, (
        data["goles_local"],
        data["goles_visitante"],
        partido_id
    ))

    cursor.close()
    conn.close()