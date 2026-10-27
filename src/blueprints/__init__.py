from blueprints.alumnos.routes import alumnos_bp
from blueprints.maestros.routes import maestros_bp
from blueprints.administrativos.routes import administrativos_bp

def registrar_blueprints(app):
    app.register_blueprint(alumnos_bp)
    app.register_blueprint(maestros_bp)
    app.register_blueprint(administrativos_bp)