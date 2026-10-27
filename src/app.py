from flask import Flask
from flask_cors import CORS

from config import config
from database import mysql
from blueprints import registrar_blueprints

app = Flask(__name__)

app.config.from_object(config['development'])

CORS(app)

mysql.init_app(app)

registrar_blueprints(app)

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>"

app.register_error_handler(404, pagina_no_encontrada)

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000
    )