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
# VERIFICAR PARTIDO DUPLICADO
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
# CREAR PARTIDO
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
# OBTENER PARTIDO POR ID
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
# REEMPLAZAR PARTIDO (PUT)
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
# ACTUALIZAR PARCIALMENTE PARTIDO (PATCH)
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
# ELIMINAR PARTIDO
# =====================================================

def delete_partido(partido_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM partidos WHERE id = %s", (partido_id,))

    cursor.close()
    conn.close()


# =====================================================
# ACTUALIZAR RESULTADO DE PARTIDO
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


# =====================================================
# LISTAR USUARIOS
# =====================================================

def get_usuarios(limit, offset):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios LIMIT %s OFFSET %s",
        (limit, offset)
    )

    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result


# =====================================================
# OBTENER USUARIO POR ID
# =====================================================

def get_usuario_by_id(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (usuario_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


# =====================================================
# OBTENER USUARIO POR EMAIL
# =====================================================

def get_usuario_by_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


# =====================================================
# CREAR USUARIO
# =====================================================

def create_usuario(data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nombre, email)
        VALUES (%s, %s)
    """, (data["nombre"], data["email"]))

    cursor.close()
    conn.close()


# =====================================================
# REEMPLAZAR USUARIO (PUT)
# =====================================================

def replace_usuario(usuario_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE usuarios
        SET nombre = %s,
            email = %s
        WHERE id = %s
    """, (data["nombre"], data["email"], usuario_id))

    cursor.close()
    conn.close()


# =====================================================
# ELIMINAR USUARIO
# =====================================================

def delete_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = %s", (usuario_id,))

    cursor.close()
    conn.close()


# =====================================================
# VERIFICAR PREDICCION EXISTENTE
# =====================================================

def get_prediccion_existente(usuario_id, partido_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM predicciones
        WHERE usuario_id = %s AND partido_id = %s
    """, (usuario_id, partido_id))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


# =====================================================
# CREAR PREDICCION
# =====================================================

def create_prediccion(usuario_id, partido_id, data):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predicciones (
            usuario_id,
            partido_id,
            goles_local,
            goles_visitante
        ) VALUES (%s, %s, %s, %s)
    """, (
        usuario_id,
        partido_id,
        data["goles_local"],
        data["goles_visitante"]
    ))

    cursor.close()
    conn.close()

# =====================================================
# OBTENER RANKING
# =====================================================

def get_ranking(limit, offset):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT 
            u.id AS usuario_id,
            COALESCE(SUM(
                CASE
                    -- resultado exacto
                    WHEN p.goles_local = pa.goles_local 
                     AND p.goles_visitante = pa.goles_visitante THEN 3
                    
                    -- resultado correcto (ganador o empate)
                    WHEN (
                        (p.goles_local > p.goles_visitante AND pa.goles_local > pa.goles_visitante) OR
                        (p.goles_local < p.goles_visitante AND pa.goles_local < pa.goles_visitante) OR
                        (p.goles_local = p.goles_visitante AND pa.goles_local = pa.goles_visitante)
                    ) THEN 1
                    
                    ELSE 0
                END
            ), 0) AS puntos
        FROM usuarios u
        LEFT JOIN predicciones p ON u.id = p.usuario_id
        LEFT JOIN partidos pa ON pa.id = p.partido_id
        WHERE pa.goles_local IS NOT NULL
        GROUP BY u.id
        ORDER BY puntos DESC
        LIMIT %s OFFSET %s
    """

    cursor.execute(query, (limit, offset))
    result = cursor.fetchall()

    cursor.close()
    conn.close()

    return result