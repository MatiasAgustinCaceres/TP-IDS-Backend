from flask import request, jsonify
from models import get_partidos


def register_routes(app):

    @app.route("/partidos", methods=["GET"])
    def listar_partidos():

        equipo = request.args.get("equipo")
        fecha = request.args.get("fecha")
        fase = request.args.get("fase")

        limit = request.args.get("limit", 10)
        offset = request.args.get("offset", 0)

        limit = int(limit)
        offset = int(offset)

        filtros = {
            "equipo": equipo,
            "fecha": fecha,
            "fase": fase
        }

        partidos = get_partidos(filtros, limit, offset)

        if not partidos:
            return {"message": "No hay partidos"}, 204

        return jsonify(partidos), 200
