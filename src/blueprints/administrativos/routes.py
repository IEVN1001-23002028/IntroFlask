from flask import Blueprint, jsonify, request
from database import mysql

administrativos_bp = Blueprint(
    'administrativos',
    __name__,
    url_prefix='/api/administrativos'
)

def fila_a_diccionario(cursor, fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas, fila))


def leer_administrativo_bd(numempleado):
    try:
        cursor = mysql.connection.cursor()

        sql = "SELECT * FROM administrativos WHERE numempleado = %s"

        cursor.execute(sql, (numempleado,))

        datos = cursor.fetchone()

        if datos != None:
            administrativo = {
                "numempleado": datos[0],
                "nombre": datos[1],
                "apellidos": datos[2],
                "telefono": datos[3],
                "correo": datos[4],
                "departamento": datos[5]
            }

            return administrativo

        else:
            return None

    except Exception as ex:
        raise ex


@administrativos_bp.route('/', methods=['GET'])
def lista_administrativos():
    cursor = None

    try:
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT numempleado, nombre, apellidos, teléfono, correo, departamento
            FROM administrativos
        """)

        datos = cursor.fetchall()

        administrativos = [
            fila_a_diccionario(cursor, fila)
            for fila in datos
        ]

        return jsonify({
            'administrativos': administrativos,
            'mensaje': 'Lista de administrativos',
            'exito': True
        }), 200

    except Exception as ex:
        return jsonify({
            'mensaje': f'Error al consultar los administrativos: {ex}',
            'exito': False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@administrativos_bp.route('/<numempleado>', methods=['GET'])
def leer_administrativo(numempleado):
    try:
        administrativo = leer_administrativo_bd(numempleado)

        if administrativo != None:
            return jsonify({
                'administrativo': administrativo,
                'mensaje': 'Administrativo encontrado',
                'exito': True
            })

        else:
            return jsonify({
                'administrativo': administrativo,
                'mensaje': 'Administrativo no encontrado',
                'exito': False
            })

    except Exception as ex:
        return jsonify({
            'message': f"error {ex}",
            'exito': False
        })


@administrativos_bp.route('/', methods=['POST'])
def registrar_administrativo():
    try:
        administrativo = leer_administrativo_bd(
            request.json['numempleado']
        )

        if administrativo != None:
            return jsonify({
                'mensaje': 'Administrativo ya existente, no se puede registrar',
                'exito': False
            })

        else:
            cursor = mysql.connection.cursor()

            sql = """
                INSERT INTO administrativos
                (numempleado, nombre, apellidos, teléfono, correo, departamento)
                VALUES (%s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                request.json['numempleado'],
                request.json['nombre'],
                request.json['apellidos'],
                request.json['telefono'],
                request.json['correo'],
                request.json['departamento']
            ))

            mysql.connection.commit()

            return jsonify({
                'mensaje': "Administrativo registrado",
                'exito': True
            })

    except Exception as ex:
        return jsonify({
            'message': f"error {ex}",
            'exito': False
        })


@administrativos_bp.route('/<numempleado>', methods=['PUT'])
def actualizar_administrativo(numempleado):
    try:
        administrativo = leer_administrativo_bd(numempleado)

        if administrativo != None:
            cursor = mysql.connection.cursor()

            sql = """
                UPDATE administrativos
                SET nombre = %s,
                    apellidos = %s,
                    teléfono = %s,
                    correo = %s,
                    departamento = %s
                WHERE numempleado = %s
            """

            cursor.execute(sql, (
                request.json['nombre'],
                request.json['apellidos'],
                request.json['telefono'],
                request.json['correo'],
                request.json['departamento'],
                numempleado
            ))

            mysql.connection.commit()

            return jsonify({
                'mensaje': "Administrativo actualizado.",
                'exito': True
            })

        else:
            return jsonify({
                'mensaje': "Administrativo no encontrado.",
                'exito': False
            })

    except Exception as ex:
        return jsonify({
            'mensaje': f"Error {ex}",
            'exito': False
        })


@administrativos_bp.route('/<numempleado>', methods=['DELETE'])
def eliminar_administrativo(numempleado):
    try:
        administrativo = leer_administrativo_bd(numempleado)

        if administrativo != None:
            cursor = mysql.connection.cursor()

            sql = "DELETE FROM administrativos WHERE numempleado = %s"

            cursor.execute(sql, (numempleado,))

            mysql.connection.commit()

            return jsonify({
                'mensaje': "Administrativo eliminado",
                'exito': True
            })

        else:
            return jsonify({
                'mensaje': "Administrativo no encontrado para eliminar",
                'exito': False
            })

    except Exception as ex:
        return jsonify({
            'mensaje': f"Error: {ex}",
            'exito': False
        })