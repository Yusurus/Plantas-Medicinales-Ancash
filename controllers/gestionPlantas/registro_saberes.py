from flask import Flask, render_template, request, jsonify,Blueprint
from config.db import get_connection
import mysql.connector

registro_saberes = Blueprint("registro_saberes", __name__)

@registro_saberes.route('/api/plantas', methods=['GET'])
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

@registro_saberes.route('/api/saberes/<int:planta_id>', methods=['GET'])
def get_saberes_planta(planta_id):
    """Obtener saberes culturales de una planta específica"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            sc.idSaberes,
            sc.descripcionSaber,
            p.nombreCientifico,
            fp.nomFamilia
        FROM saberes_culturales sc
        JOIN plantas p ON sc.fk_plantas = p.idPlanta
        LEFT JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        WHERE sc.fk_plantas = %s
        ORDER BY sc.idSaberes DESC
        """
        
        cursor.execute(query, (planta_id,))
        saberes = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify(saberes)
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_saberes.route('/api/saberes', methods=['POST'])
def add_saber_cultural():
    """Añadir un nuevo saber cultural"""
    try:
        data = request.get_json()
        
        if not data or 'descripcionSaber' not in data or 'fk_plantas' not in data:
            return jsonify({'error': 'Datos incompletos'}), 400
        
        descripcion = data['descripcionSaber'].strip()
        planta_id = data['fk_plantas']
        
        if not descripcion:
            return jsonify({'error': 'La descripción no puede estar vacía'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar que la planta existe
        cursor.execute("SELECT idPlanta FROM plantas WHERE idPlanta = %s", (planta_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'La planta especificada no existe'}), 404
        
        # Insertar el nuevo saber cultural
        query = """
        INSERT INTO saberes_culturales (descripcionSaber, fk_plantas)
        VALUES (%s, %s)
        """
        
        cursor.execute(query, (descripcion, planta_id))
        conn.commit()
        
        # Obtener el ID del saber recién insertado
        nuevo_id = cursor.lastrowid
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Saber cultural añadido exitosamente',
            'id': nuevo_id
        }), 201
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_saberes.route('/api/saberes/<int:saber_id>', methods=['PUT'])
def update_saber_cultural(saber_id):
    """Actualizar un saber cultural existente"""
    try:
        data = request.get_json()
        
        if not data or 'descripcionSaber' not in data:
            return jsonify({'error': 'Descripción requerida'}), 400
        
        descripcion = data['descripcionSaber'].strip()
        
        if not descripcion:
            return jsonify({'error': 'La descripción no puede estar vacía'}), 400
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar que el saber existe
        cursor.execute("SELECT idSaberes FROM saberes_culturales WHERE idSaberes = %s", (saber_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Saber cultural no encontrado'}), 404
        
        # Actualizar el saber cultural
        query = """
        UPDATE saberes_culturales 
        SET descripcionSaber = %s 
        WHERE idSaberes = %s
        """
        
        cursor.execute(query, (descripcion, saber_id))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Saber cultural actualizado exitosamente'
        })
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500

@registro_saberes.route('/api/saberes/<int:saber_id>', methods=['DELETE'])
def delete_saber_cultural(saber_id):
    """Eliminar un saber cultural"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Verificar que el saber existe
        cursor.execute("SELECT idSaberes FROM saberes_culturales WHERE idSaberes = %s", (saber_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Saber cultural no encontrado'}), 404
        
        # Eliminar el saber cultural
        cursor.execute("DELETE FROM saberes_culturales WHERE idSaberes = %s", (saber_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Saber cultural eliminado exitosamente'
        })
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Error de base de datos: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error inesperado: {str(e)}'}), 500