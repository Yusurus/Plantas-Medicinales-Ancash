from flask import request, jsonify, Blueprint
from config.db import get_connection
import mysql.connector

registro_usos = Blueprint("registro_usos", __name__)

@registro_usos.route('/api/plantas', methods=['GET'])
def get_plantas():
    """Obtener todas las plantas con sus nombres científicos y comunes"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT DISTINCT 
            p.idPlanta,
            p.nombreCientifico,
            fp.nomFamilia,
            GROUP_CONCAT(nc.nombreComun SEPARATOR ', ') as nombresComunes
        FROM plantas p
        LEFT JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        GROUP BY p.idPlanta, p.nombreCientifico, fp.nomFamilia
        ORDER BY p.nombreCientifico
        """
        
        cursor.execute(query)
        plantas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(plantas)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_usos.route('/api/usos/<int:planta_id>', methods=['GET'])
def get_usos_planta(planta_id):
    """Obtener todos los usos de una planta específica"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            u.idUsos,
            u.parte,
            u.uso,
            u.contraIndicaciones,
            u.preparacion,
            p.nombreCientifico,
            fp.nomFamilia,
            GROUP_CONCAT(nc.nombreComun SEPARATOR ', ') as nombresComunes
        FROM usos u
        JOIN plantas p ON u.fk_plantas = p.idPlanta
        LEFT JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        WHERE u.fk_plantas = %s
        GROUP BY u.idUsos, u.parte, u.uso, u.contraIndicaciones, u.preparacion, 
                 p.nombreCientifico, fp.nomFamilia
        ORDER BY u.idUsos DESC
        """
        
        cursor.execute(query, (planta_id,))
        usos = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(usos)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_usos.route('/api/usos', methods=['GET'])
def get_todos_usos():
    """Obtener todos los usos registrados con información de la planta"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            u.idUsos,
            u.parte,
            u.uso,
            u.contraIndicaciones,
            u.preparacion,
            u.fk_plantas,
            p.nombreCientifico,
            fp.nomFamilia,
            GROUP_CONCAT(nc.nombreComun SEPARATOR ', ') as nombresComunes
        FROM usos u
        JOIN plantas p ON u.fk_plantas = p.idPlanta
        LEFT JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        GROUP BY u.idUsos, u.parte, u.uso, u.contraIndicaciones, u.preparacion, 
                 u.fk_plantas, p.nombreCientifico, fp.nomFamilia
        ORDER BY p.nombreCientifico, u.parte
        """
        
        cursor.execute(query)
        usos = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(usos)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500
    
    
@registro_usos.route('/api/usos', methods=['POST'])
def add_uso():
    """Añadir un nuevo uso para una planta usando procedimiento almacenado"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['parte', 'uso', 'contraIndicaciones', 'preparacion', 'fk_plantas']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Datos incompletos. Se requieren: parte, uso, contraIndicaciones, preparacion, fk_plantas'}), 400
        
        parte = data['parte'].strip()
        uso = data['uso'].strip()
        contra_indicaciones = data['contraIndicaciones'].strip()
        preparacion = data['preparacion'].strip()
        planta_id = data['fk_plantas']
        
        # Validar que los campos no estén vacíos
        if not all([parte, uso, contra_indicaciones, preparacion]):
            return jsonify({'error': 'Ningún campo puede estar vacío'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado
        cursor.callproc('insertar_uso', [parte, uso, contra_indicaciones, preparacion, planta_id])
        
        # Obtener el ID del último registro insertado
        nuevo_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Uso añadido exitosamente',
            'id': nuevo_id
        }), 201
    
    except mysql.connector.Error as e:
        error_msg = str(e)
        
        # Determinar el código de estado según el mensaje de error
        if 'no existe' in error_msg:
            return jsonify({'error': error_msg}), 404
        elif any(msg in error_msg for msg in ['no puede estar vacía', 'no puede estar vacío', 'especificar una planta válida']):
            return jsonify({'error': error_msg}), 400
        else:
            return jsonify({'error': f'Error de base de datos: {error_msg}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

# @registro_usos.route('/api/usos', methods=['POST'])
# def add_uso():
#     """Añadir un nuevo uso para una planta"""
#     try:
#         data = request.get_json()
        
#         # Validar datos requeridos
#         required_fields = ['parte', 'uso', 'contraIndicaciones', 'preparacion', 'fk_plantas']
#         if not data or not all(field in data for field in required_fields):
#             return jsonify({'error': 'Datos incompletos. Se requieren: parte, uso, contraIndicaciones, preparacion, fk_plantas'}), 400
        
#         parte = data['parte'].strip()
#         uso = data['uso'].strip()
#         contra_indicaciones = data['contraIndicaciones'].strip()
#         preparacion = data['preparacion'].strip()
#         planta_id = data['fk_plantas']
        
#         # Validar que los campos no estén vacíos
#         if not all([parte, uso, contra_indicaciones, preparacion]):
#             return jsonify({'error': 'Ningún campo puede estar vacío'}), 400
        
#         conn = get_connection()
#         cursor = conn.cursor()
        
#         # Verificar que la planta existe
#         cursor.execute("SELECT idPlanta FROM plantas WHERE idPlanta = %s", (planta_id,))
#         if not cursor.fetchone():
#             cursor.close()
#             conn.close()
#             return jsonify({'error': 'La planta especificada no existe'}), 404
        
#         # Insertar el nuevo uso
#         query = """
#         INSERT INTO usos (parte, uso, contraIndicaciones, preparacion, fk_plantas)
#         VALUES (%s, %s, %s, %s, %s)
#         """
        
#         cursor.execute(query, (parte, uso, contra_indicaciones, preparacion, planta_id))
#         conn.commit()
        
#         # Obtener el ID del uso recién insertado
#         nuevo_id = cursor.lastrowid
        
#         cursor.close()
#         conn.close()
        
#         return jsonify({
#             'success': True,
#             'message': 'Uso añadido exitosamente',
#             'id': nuevo_id
#         }), 201
    
#     except mysql.connector.Error as e:
#         return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
#     except Exception as e:
#         return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_usos.route('/api/usos/<int:uso_id>', methods=['GET'])
def get_uso_by_id(uso_id):
    """Obtener un uso específico por su ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            u.idUsos,
            u.parte,
            u.uso,
            u.contraIndicaciones,
            u.preparacion,
            u.fk_plantas,
            p.nombreCientifico,
            fp.nomFamilia,
            GROUP_CONCAT(nc.nombreComun SEPARATOR ', ') as nombresComunes
        FROM usos u
        JOIN plantas p ON u.fk_plantas = p.idPlanta
        LEFT JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        WHERE u.idUsos = %s
        GROUP BY u.idUsos, u.parte, u.uso, u.contraIndicaciones, u.preparacion, 
                 u.fk_plantas, p.nombreCientifico, fp.nomFamilia
        """
        
        cursor.execute(query, (uso_id,))
        uso = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if not uso:
            return jsonify({'error': 'Uso no encontrado'}), 404
        
        return jsonify(uso)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_usos.route('/api/usos/<int:uso_id>', methods=['PUT'])
def update_uso(uso_id):
    """Actualizar un uso existente"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['parte', 'uso', 'contraIndicaciones', 'preparacion']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'error': 'Datos incompletos. Se requieren: parte, uso, contraIndicaciones, preparacion'}), 400
        
        parte = data['parte'].strip()
        uso = data['uso'].strip()
        contra_indicaciones = data['contraIndicaciones'].strip()
        preparacion = data['preparacion'].strip()
        
        # Validar que los campos no estén vacíos
        if not all([parte, uso, contra_indicaciones, preparacion]):
            return jsonify({'error': 'Ningún campo puede estar vacío'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar que el uso existe
        cursor.execute("SELECT idUsos FROM usos WHERE idUsos = %s", (uso_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Uso no encontrado'}), 404
        
        # Actualizar el uso
        query = """
        UPDATE usos 
        SET parte = %s, uso = %s, contraIndicaciones = %s, preparacion = %s
        WHERE idUsos = %s
        """
        
        cursor.execute(query, (parte, uso, contra_indicaciones, preparacion, uso_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Uso actualizado exitosamente'
        })
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_usos.route('/api/usos/<int:uso_id>', methods=['DELETE'])
def delete_uso(uso_id):
    """Eliminar un uso"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar que el uso existe
        cursor.execute("SELECT idUsos FROM usos WHERE idUsos = %s", (uso_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Uso no encontrado'}), 404
        
        # Eliminar el uso
        cursor.execute("DELETE FROM usos WHERE idUsos = %s", (uso_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Uso eliminado exitosamente'
        })
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_usos.route('/api/buscar-usos', methods=['GET'])
def buscar_usos():
    """Buscar usos por diferentes criterios"""
    try:
        # Obtener parámetros de búsqueda
        planta_nombre = request.args.get('planta', '').strip()
        parte = request.args.get('parte', '').strip()
        uso_tipo = request.args.get('uso', '').strip()
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Construir query dinámicamente
        base_query = """
        SELECT 
            u.idUsos,
            u.parte,
            u.uso,
            u.contraIndicaciones,
            u.preparacion,
            u.fk_plantas,
            p.nombreCientifico,
            fp.nomFamilia,
            GROUP_CONCAT(nc.nombreComun SEPARATOR ', ') as nombresComunes
        FROM usos u
        JOIN plantas p ON u.fk_plantas = p.idPlanta
        LEFT JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        """
        
        conditions = []
        params = []
        
        if planta_nombre:
            conditions.append("(p.nombreCientifico LIKE %s OR nc.nombreComun LIKE %s)")
            params.extend([f'%{planta_nombre}%', f'%{planta_nombre}%'])
        
        if parte:
            conditions.append("u.parte LIKE %s")
            params.append(f'%{parte}%')
        
        if uso_tipo:
            conditions.append("u.uso LIKE %s")
            params.append(f'%{uso_tipo}%')
        
        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)
        
        base_query += """
        GROUP BY u.idUsos, u.parte, u.uso, u.contraIndicaciones, u.preparacion, 
                 u.fk_plantas, p.nombreCientifico, fp.nomFamilia
        ORDER BY p.nombreCientifico, u.parte
        """
        
        cursor.execute(base_query, params)
        resultados = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(resultados)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_usos.route('/api/usos-por-parte', methods=['GET'])
def get_usos_por_parte():
    """Obtener estadísticas de usos agrupados por parte de la planta"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            u.parte,
            COUNT(*) as cantidad_usos,
            COUNT(DISTINCT u.fk_plantas) as plantas_diferentes
        FROM usos u
        GROUP BY u.parte
        ORDER BY cantidad_usos DESC
        """
        
        cursor.execute(query)
        estadisticas = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(estadisticas)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500