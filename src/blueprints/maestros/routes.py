from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))


def leer_maestro_bd(idmaestro):
    try:
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM maestros WHERE idmaestro = %s"

        cursor.execute(sql, (idmaestro,))

        datos = cursor.fetchone()

        if datos != None:
            maestro = {
                "idmaestro": datos[0],
                "nombre": datos[1],
                "apaterno": datos[2],
                "amaterno": datos[3],
                "correo": datos[4]
            }

            return maestro

        else:
            return None

    except Exception as ex:
        raise ex


@maestros_bp.route('/', methods=['GET'])
def lista_maestros():
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT idmaestro, nombre, apaterno, amaterno, correo
            FROM maestros
        """)

        datos = cursor.fetchall()

        maestros = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': f'Error al consultar los maestros: {ex}',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@maestros_bp.route('/<idmaestro>', methods=['GET'])
def leer_maestro(idmaestro):
    try:
        maestro = leer_maestro_bd(idmaestro)

        if maestro != None:
            return jsonify({
                'maestro': maestro,
                'mensaje': 'Maestro encontrado',
                'exito': True
            })

        else:
            return jsonify({
                'maestro': maestro,
                'mensaje': 'Maestro no encontrado',
                'exito': False
            })

    except Exception as ex:
        return jsonify({
            'message': f"error {ex}",
            'exito': False
        })


@maestros_bp.route('/', methods=['POST'])
def registrar_maestro():
    try:
        maestro = leer_maestro_bd(request.json['idmaestro'])

        if maestro != None:
            return jsonify({
                'mensaje': 'Maestro ya existente, no se puede registrar',
                'exito': False
            })

        else:
            cursor = mysql.connection.cursor()

            sql = """
                INSERT INTO maestros
                (idmaestro, nombre, apaterno, amaterno, correo)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                request.json['idmaestro'],
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo']
            ))

            mysql.connection.commit()

            return jsonify({
                'mensaje': "Maestro registrado",
                'exito': True
            })

    except Exception as ex:
        return jsonify({
            'message': f"error {ex}",
            'exito': False
        })


@maestros_bp.route('/<idmaestro>', methods=['PUT'])
def actualizar_maestro(idmaestro):
    try:
        maestro = leer_maestro_bd(idmaestro)

        if maestro != None:
            cursor = mysql.connection.cursor()

            sql = """
                UPDATE maestros
                SET nombre = %s,
                    apaterno = %s,
                    amaterno = %s,
                    correo = %s
                WHERE idmaestro = %s
            """

            cursor.execute(sql, (
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo'],
                idmaestro
            ))

            mysql.connection.commit()

            return jsonify({
                'mensaje': "Maestro actualizado.",
                'exito': True
            })

        else:
            return jsonify({
                'mensaje': "Maestro no encontrado.",
                'exito': False
            })

    except Exception as ex:
        return jsonify({
            'mensaje': f"Error {ex}",
            'exito': False
        })


@maestros_bp.route('/<idmaestro>', methods=['DELETE'])
def eliminar_maestro(idmaestro):
    try:
        maestro = leer_maestro_bd(idmaestro)

        if maestro != None:
            cursor = mysql.connection.cursor()

            sql = "DELETE FROM maestros WHERE idmaestro = %s"

            cursor.execute(sql, (idmaestro,))

            mysql.connection.commit()

            return jsonify({
                'mensaje': "Maestro eliminado",
                'exito': True
            })

        else:
            return jsonify({
                'mensaje': "Maestro no encontrado para eliminar",
                'exito': False
            })

    except Exception as ex:
        return jsonify({
            'mensaje': f"Error: {ex}",
            'exito': False
        })