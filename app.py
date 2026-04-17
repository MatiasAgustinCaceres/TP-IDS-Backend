from flask import Flask
from routes import register_routes
from db_conection import init_db

app = Flask(__name__)

# inicializar base de datos
init_db()

# registrar rutas
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)