from flask import request, jsonify
from models import (
    get_partidos,
    create_partido,
    get_partido_existente,
    get_partido_by_id,
    replace_partido,
    patch_partido,
    delete_partido,
    update_resultado,
    get_usuario_by_id,
    get_usuarios,
    get_usuario_by_email,
    create_usuario,
    replace_usuario,
    delete_usuario,
    get_prediccion_existente,
    create_prediccion,
    get_ranking
)


def register_routes(app):

    # =====================================================
    # GET /partidos
    # =====================================================
    @app.route("/partidos", methods=["GET"])
    def listar_partidos():
        try:
            equipo = request.args.get("equipo")
            fecha = request.args.get("fecha")
            fase = request.args.get("fase")

            limit = int(request.args.get("limit", 10))
            offset = int(request.args.get("offset", 0))

            if limit < 0 or offset < 0:
                return {"error": "Parámetros inválidos"}, 400

            filtros = {
                "equipo": equipo,
                "fecha": fecha,
                "fase": fase
            }

            partidos = get_partidos(filtros, limit, offset)

            if not partidos:
                return "", 204

            return jsonify(partidos), 200

        except:
            return {"error": "Error interno"}, 500


    # =====================================================
    # POST /partidos
    # =====================================================
    @app.route("/partidos", methods=["POST"])
    def crear_partido():
        try:
            data = request.get_json()

            if not data:
                return {"error": "Body vacío"}, 400

            required = ["equipo_local", "equipo_visitante", "fecha", "fase"]

            for r in required:
                if r not in data:
                    return {"error": f"Falta {r}"}, 400

            if get_partido_existente(data):
                return {"error": "Partido duplicado"}, 409

            create_partido(data)

            return {"message": "Partido creado"}, 201

        except:
            return {"error": "Error interno"}, 500


    # =====================================================
    # GET /partidos/{id}
    # =====================================================
    @app.route("/partidos/<id>", methods=["GET"])
    def obtener_partido(id):
        try:
            if not id.isdigit():
                return {"error": "ID inválido"}, 400

            partido = get_partido_by_id(id)

            if not partido:
                return {"error": "No encontrado"}, 404

            return jsonify(partido), 200

        except:
            return {"error": "Error interno"}, 500


    # =====================================================
    # PUT /partidos/{id}
    # =====================================================
    @app.route("/partidos/<int:id>", methods=["PUT"])
    def reemplazar_partido(id):
        try:
            data = request.get_json()

            if not data:
                return {"error": "Body vacío"}, 400

            required = ["equipo_local", "equipo_visitante", "fecha", "fase"]

            for r in required:
                if r not in data:
                    return {"error": f"Falta {r}"}, 400

            if not get_partido_by_id(id):
                return {"error": "No encontrado"}, 404

            replace_partido(id, data)

            return "", 204

        except:
            return {"error": "Error interno"}, 500


    # =====================================================
    # PATCH /partidos/{id}
    # =====================================================
    @app.route("/partidos/<int:id>", methods=["PATCH"])
    def actualizar_parcial_partido(id):
        try:
            data = request.get_json()

            if not data:
                return {"error": "Body vacío"}, 400

            if not get_partido_by_id(id):
                return {"error": "No encontrado"}, 404

            patch_partido(id, data)

            return "", 204

        except:
            return {"error": "Error interno"}, 500


    # =====================================================
    # DELETE /partidos/{id}
    # =====================================================
    @app.route("/partidos/<id>", methods=["DELETE"])
    def eliminar_partido(id):
        try:
            if not id.isdigit():
                return {"error": "ID inválido"}, 400

            if not get_partido_by_id(id):
                return {"error": "No encontrado"}, 404

            delete_partido(id)

            return "", 204

        except:
            return {"error": "Error interno"}, 500


    # =====================================================
    # PUT /partidos/{id}/resultado
    # =====================================================
    @app.route("/partidos/<id>/resultado", methods=["PUT"])
    def actualizar_resultado_partido(id):
        try:
            if not id.isdigit():
                return {"error": "ID inválido"}, 400

            data = request.get_json()

            if not data:
                return {"error": "Body vacío"}, 400

            required = ["goles_local", "goles_visitante"]

            for r in required:
                if r not in data:
                    return {"error": f"Falta {r}"}, 400

            partido = get_partido_by_id(id)

            if not partido:
                return {"error": "No encontrado"}, 404

            update_resultado(id, data)

            return "", 204

        except:
            return {"error": "Error interno"}, 500


    # =====================================================
    # GET /usuarios
    # =====================================================
    @app.route("/usuarios", methods=["GET"])
    def listar_usuarios():
        try:
            limit = int(request.args.get("limit", 10))
            offset = int(request.args.get("offset", 0))

            if limit < 0 or offset < 0:
                return {"error": "Parámetros inválidos"}, 400

            usuarios = get_usuarios(limit, offset)

            if not usuarios:
                return "", 204

            return jsonify(usuarios), 200

        except:
            return {"error": "Error interno"}, 500


    # =====================================================
    # POST /usuarios
    # =====================================================
    @app.route("/usuarios", methods=["POST"])
    def crear_usuario():
        try:
            data = request.get_json()

            if not data:
                return {"error": "Body vacío"}, 400

            required = ["nombre", "email"]

            for r in required:
                if r not in data:
                    return {"error": f"Falta {r}"}, 400

            if get_usuario_by_email(data["email"]):
                return {"error": "Email ya existe"}, 409

            create_usuario(data)

            return {"message": "Usuario creado"}, 201

        except:
            return {"error": "Error interno"}, 500


    # =====================================================
    # GET /usuarios/{id}
    # =====================================================
    @app.route("/usuarios/<id>", methods=["GET"])
    def obtener_usuario(id):
        try:
            if not id.isdigit():
                return {"error": "ID inválido"}, 400

            usuario = get_usuario_by_id(id)

            if not usuario:
                return {"error": "No encontrado"}, 404

            return jsonify(usuario), 200

        except:
            return {"error": "Error interno"}, 500


    # =====================================================
    # PUT /usuarios/{id}
    # =====================================================
    @app.route("/usuarios/<int:id>", methods=["PUT"])
    def reemplazar_usuario(id):
        try:
            data = request.get_json()

            if not data:
                return {"error": "Body vacío"}, 400

            required = ["nombre", "email"]

            for r in required:
                if r not in data:
                    return {"error": f"Falta {r}"}, 400

            usuario_existente = get_usuario_by_email(data["email"])
            if usuario_existente and usuario_existente["id"] != id:
                return {"error": "Email ya existe"}, 409

            if get_usuario_by_id(id):
                replace_usuario(id, data)
            else:
                create_usuario(data)

            return "", 204

        except:
            return {"error": "Error interno"}, 500


    # =====================================================
    # DELETE /usuarios/{id}
    # =====================================================
    @app.route("/usuarios/<id>", methods=["DELETE"])
    def eliminar_usuario(id):
        try:
            if not id.isdigit():
                return {"error": "ID inválido"}, 400

            if not get_usuario_by_id(id):
                return {"error": "No encontrado"}, 404

            delete_usuario(id)

            return "", 204

        except:
            return {"error": "Error interno"}, 500


    # =====================================================
    # POST /partidos/{id}/prediccion
    # =====================================================
    @app.route("/partidos/<id>/prediccion", methods=["POST"])
    def crear_prediccion(id):
        try:
            if not id.isdigit():
                return {"error": "ID inválido"}, 400

            data = request.get_json()

            if not data:
                return {"error": "Body vacío"}, 400

            required = ["usuario_id", "goles_local", "goles_visitante"]

            for r in required:
                if r not in data:
                    return {"error": f"Falta {r}"}, 400

            partido = get_partido_by_id(id)
            if not partido:
                return {"error": "Partido no encontrado"}, 404

            usuario = get_usuario_by_id(data["usuario_id"])
            if not usuario:
                return {"error": "Usuario no encontrado"}, 404

            if partido["goles_local"] is not None:
                return {"error": "El partido ya tiene resultado"}, 400

            if get_prediccion_existente(data["usuario_id"], id):
                return {"error": "Predicción ya existente"}, 409

            create_prediccion(data["usuario_id"], id, data)

            return {"message": "Predicción creada"}, 201

        except:
            return {"error": "Error interno"}, 500

    # =====================================================
    # GET /ranking
    # =====================================================
    @app.route("/ranking", methods=["GET"])
    def obtener_ranking():
        try:
            limit = int(request.args.get("limit", 10))
            offset = int(request.args.get("offset", 0))

            if limit < 0 or offset < 0:
                return {"error": "Parámetros inválidos"}, 400

            ranking = get_ranking(limit, offset)

            if not ranking:
                return "", 204

            return jsonify(ranking), 200

        except:
            return {"error": "Error interno"}, 500