from flask import request, jsonify, Blueprint
from config.db import get_connection
import mysql.connector

# Crear el blueprint
registro_zona = Blueprint("registro_zona", __name__)

@registro_zona.route('/api/todas_plantas_zonas', methods=['GET'])
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
    
@registro_zona.route('/api/ecoregiones', methods=['GET'])
def get_ecoregiones():
    """Obtener todas las ecoregiones"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.callproc('visor_ecoregiones')
        
        # Obtener resultados del procedimiento almacenado
        results = []
        for result in cursor.stored_results():
            results = result.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(results)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

# ==================== CRUD REGIONES ====================

@registro_zona.route('/api/regiones', methods=['GET'])
def get_regiones():
    """Obtener todas las regiones"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.callproc('visor_regiones')
        
        # Obtener resultados del procedimiento almacenado
        results = []
        for result in cursor.stored_results():
            results = result.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(results)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_zona.route('/api/regiones', methods=['POST'])
def crear_region():
    """Crear una nueva región"""
    try:
        data = request.get_json()
        
        if not data or 'region' not in data:
            return jsonify({'error': 'El campo "region" es requerido'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado para insertar
        cursor.callproc('crud_regiones', [1, None, data['region']])
        
        # Obtener el mensaje de resultado
        for result in cursor.stored_results():
            mensaje = result.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': mensaje[0] if mensaje else 'Región creada exitosamente'}), 201
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_zona.route('/api/regiones/<int:id_region>', methods=['PUT'])
def actualizar_region(id_region):
    """Actualizar una región existente"""
    try:
        data = request.get_json()
        
        if not data or 'region' not in data:
            return jsonify({'error': 'El campo "region" es requerido'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado para actualizar
        cursor.callproc('crud_regiones', [2, id_region, data['region']])
        
        # Obtener el mensaje de resultado
        for result in cursor.stored_results():
            mensaje = result.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': mensaje[0] if mensaje else 'Región actualizada exitosamente'})
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_zona.route('/api/regiones/<int:id_region>', methods=['DELETE'])
def eliminar_region(id_region):
    """Eliminar una región"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado para eliminar
        cursor.callproc('crud_regiones', [3, id_region, None])
        
        # Obtener el mensaje de resultado
        for result in cursor.stored_results():
            mensaje = result.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': mensaje[0] if mensaje else 'Región eliminada exitosamente'})
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

# ==================== CRUD PROVINCIAS ====================

@registro_zona.route('/api/regiones/<int:id_region>/provincias', methods=['GET'])
def get_provincias_por_region(id_region):
    """Obtener todas las provincias de una región"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.callproc('visor_provincias_por_region', [id_region])
        
        # Obtener resultados del procedimiento almacenado
        results = []
        for result in cursor.stored_results():
            results = result.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(results)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_zona.route('/api/provincias', methods=['POST'])
def crear_provincia():
    """Crear una nueva provincia"""
    try:
        data = request.get_json()
        
        if not data or 'nombreProvincia' not in data or 'idRegion' not in data:
            return jsonify({'error': 'Los campos "nombreProvincia" y "idRegion" son requeridos'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado para insertar
        cursor.callproc('crud_provincias', [1, None, data['nombreProvincia'], data['idRegion']])
        
        # Obtener el mensaje de resultado
        for result in cursor.stored_results():
            mensaje = result.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': mensaje[0] if mensaje else 'Provincia creada exitosamente'}), 201
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_zona.route('/api/provincias/<int:id_provincia>', methods=['PUT'])
def actualizar_provincia(id_provincia):
    """Actualizar una provincia existente"""
    try:
        data = request.get_json()
        
        if not data or 'nombreProvincia' not in data or 'idRegion' not in data:
            return jsonify({'error': 'Los campos "nombreProvincia" y "idRegion" son requeridos'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado para actualizar
        cursor.callproc('crud_provincias', [2, id_provincia, data['nombreProvincia'], data['idRegion']])
        
        # Obtener el mensaje de resultado
        for result in cursor.stored_results():
            mensaje = result.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': mensaje[0] if mensaje else 'Provincia actualizada exitosamente'})
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_zona.route('/api/provincias/<int:id_provincia>', methods=['DELETE'])
def eliminar_provincia(id_provincia):
    """Eliminar una provincia"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado para eliminar
        cursor.callproc('crud_provincias', [3, id_provincia, None, None])
        
        # Obtener el mensaje de resultado
        for result in cursor.stored_results():
            mensaje = result.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': mensaje[0] if mensaje else 'Provincia eliminada exitosamente'})
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

# ==================== PROVINCIA-ECOREGION ====================

@registro_zona.route('/api/provincias/<int:id_provincia>/ecoregiones', methods=['GET'])
def get_ecoregiones_por_provincia(id_provincia):
    """Obtener todas las ecoregiones de una provincia"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.callproc('visor_provincia_ecoregion', [id_provincia])
        
        # Obtener resultados del procedimiento almacenado
        results = []
        for result in cursor.stored_results():
            results = result.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(results)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_zona.route('/api/provincia-ecoregion', methods=['POST'])
def asociar_provincia_ecoregion():
    """Asociar una provincia con una ecoregión"""
    try:
        data = request.get_json()
        
        if not data or 'idProvincia' not in data or 'idEcoregion' not in data:
            return jsonify({'error': 'Los campos "idProvincia" y "idEcoregion" son requeridos'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado para asociar
        cursor.callproc('crud_provincia_ecoregion', [1, data['idProvincia'], data['idEcoregion']])
        
        # Obtener el mensaje de resultado
        for result in cursor.stored_results():
            mensaje = result.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': mensaje[0] if mensaje else 'Asociación creada exitosamente'}), 201
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_zona.route('/api/provincia-ecoregion', methods=['DELETE'])
def eliminar_provincia_ecoregion():
    """Eliminar asociación entre provincia y ecoregión"""
    try:
        data = request.get_json()
        
        if not data or 'idProvincia' not in data or 'idEcoregion' not in data:
            return jsonify({'error': 'Los campos "idProvincia" y "idEcoregion" son requeridos'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado para eliminar
        cursor.callproc('crud_provincia_ecoregion', [2, data['idProvincia'], data['idEcoregion']])
        
        # Obtener el mensaje de resultado
        for result in cursor.stored_results():
            mensaje = result.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': mensaje[0] if mensaje else 'Asociación eliminada exitosamente'})
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

# ==================== ECOREGION-PLANTA ====================

@registro_zona.route('/api/plantas/<int:id_planta>/ecoregiones', methods=['GET'])
def get_ecoregiones_por_planta(id_planta):
    """Obtener todas las ecoregiones de una planta"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.callproc('visor_ecoregion_planta', [1, id_planta])
        
        # Obtener resultados del procedimiento almacenado
        results = []
        for result in cursor.stored_results():
            results = result.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(results)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_zona.route('/api/ecoregiones/<int:id_ecoregion>/plantas', methods=['GET'])
def get_plantas_por_ecoregion(id_ecoregion):
    """Obtener todas las plantas de una ecoregión"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.callproc('visor_ecoregion_planta', [2, id_ecoregion])
        
        # Obtener resultados del procedimiento almacenado
        results = []
        for result in cursor.stored_results():
            results = result.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(results)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_zona.route('/api/ecoregion-planta', methods=['POST'])
def asociar_ecoregion_planta():
    """Asociar una planta con una ecoregión"""
    try:
        data = request.get_json()
        
        if not data or 'idPlanta' not in data or 'idEcoregion' not in data:
            return jsonify({'error': 'Los campos "idPlanta" y "idEcoregion" son requeridos'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado para asociar
        cursor.callproc('crud_ecoregion_planta', [1, None, data['idPlanta'], data['idEcoregion']])
        
        # Obtener el mensaje de resultado
        for result in cursor.stored_results():
            mensaje = result.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': mensaje[0] if mensaje else 'Asociación creada exitosamente'}), 201
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_zona.route('/api/ecoregion-planta/actualizar/<int:id_ecoregion_planta>', methods=['PUT'])
def actualizar_ecoregion_planta(id_ecoregion_planta):
    """Actualizar la ecoregión de una asociación planta-ecoregión"""
    try:
        data = request.get_json()
        
        if not data or 'idEcoregion' not in data:
            return jsonify({'error': 'El campo "idEcoregion" es requerido'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado para actualizar
        cursor.callproc('crud_ecoregion_planta', [2, id_ecoregion_planta, None, data['idEcoregion']])
        
        # Obtener el mensaje de resultado
        for result in cursor.stored_results():
            mensaje = result.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': mensaje[0] if mensaje else 'Asociación actualizada exitosamente'})
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500
    
@registro_zona.route('/api/ecoregion-planta/eliminar/<int:id_ecoregion_planta>', methods=['DELETE'])
def eliminarEcoregionPlanta(id_ecoregion_planta):
    """Eliminar la ecoregión de una asociación planta-ecoregión"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado para eliminar
        cursor.callproc('crud_ecoregion_planta', [3, id_ecoregion_planta, None, None])
        
        # Obtener el mensaje de resultado
        mensaje = None
        for result in cursor.stored_results():
            mensaje = result.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': mensaje[0] if mensaje else 'Eliminación exitosa'})
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_zona.route('/api/ecoregion-planta/<int:id_ecoregion_planta>', methods=['DELETE'])
def archivar_ecoregion_planta(id_ecoregion_planta):
    """Archivar una asociación planta-ecoregión"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Llamar al procedimiento almacenado para archivar
        cursor.callproc('crud_ecoregion_planta', [3, id_ecoregion_planta, None, None])
        
        # Obtener el mensaje de resultado
        for result in cursor.stored_results():
            mensaje = result.fetchone()
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': mensaje[0] if mensaje else 'Asociación archivada exitosamente'})
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500