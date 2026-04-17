from flask import request, jsonify
from models import (
    get_partidos,
    create_partido,
    get_partido_existente,
    get_partido_by_id,
    replace_partido,
    patch_partido,
    delete_partido,
    update_resultado
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

        except Exception:
            return {"error": "Error interno"}, 500


    # =====================================================
    # POST /partidos
    # =====================================================
    @app.route("/partidos", methods=["POST"])
    def crear_partido():

        try:
            data = request.get_json()

            required = ["equipo_local", "equipo_visitante", "fecha", "fase"]

            for r in required:
                if r not in data:
                    return {"error": f"Falta {r}"}, 400

            if get_partido_existente(data):
                return {"error": "Partido duplicado"}, 409

            create_partido(data)

            return {"message": "Partido creado"}, 201

        except Exception:
            return {"error": "Error interno"}, 500


    # =====================================================
    # GET /partidos/{id}
    # =====================================================
    @app.route("/partidos/<id>", methods=["GET"])
    def get_partido(id):

        try:
            if not str(id).isdigit():
                return {"error": "ID inválido"}, 400

            partido = get_partido_by_id(id)

            if not partido:
                return {"error": "No encontrado"}, 404

            return jsonify(partido), 200

        except Exception:
            return {"error": "Error interno"}, 500


    # =====================================================
    # PUT /partidos/{id}
    # =====================================================
    @app.route("/partidos/<int:id>", methods=["PUT"])
    def put_partido(id):

        try:
            data = request.get_json()

            required = ["equipo_local", "equipo_visitante", "fecha", "fase"]

            for r in required:
                if r not in data:
                    return {"error": f"Falta {r}"}, 400

            replace_partido(id, data)

            return "", 204

        except Exception:
            return {"error": "Error interno"}, 500


    # =====================================================
    # PATCH /partidos/{id}
    # =====================================================
    @app.route("/partidos/<int:id>", methods=["PATCH"])
    def patch_partido_route(id):

        try:
            data = request.get_json()

            if not data:
                return {"error": "Body vacío"}, 400

            if not get_partido_by_id(id):
                return {"error": "No encontrado"}, 404

            patch_partido(id, data)

            return "", 204

        except Exception:
            return {"error": "Error interno"}, 500


    # =====================================================
    # DELETE /partidos/{id}
    # =====================================================
    @app.route("/partidos/<id>", methods=["DELETE"])
    def delete_partido_route(id):

        try:
            if not str(id).isdigit():
                return {"error": "ID inválido"}, 400

            if not get_partido_by_id(id):
                return {"error": "No encontrado"}, 404

            delete_partido(id)

            return "", 204

        except Exception:
            return {"error": "Error interno"}, 500


    # =====================================================
    # PUT /partidos/{id}/resultado
    # =====================================================
    @app.route("/partidos/<id>/resultado", methods=["PUT"])
    def actualizar_resultado(id):

        try:
            if not str(id).isdigit():
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

        except Exception:
            return {"error": "Error interno"}, 500
