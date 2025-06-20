from flask import  request, jsonify, Blueprint
from mysql.connector import Error
from config.db import get_connection

registro_zona = Blueprint("registro_zona", __name__)

@registro_zona.route('/buscar_plantas')
def buscar_plantas():
    """Busca plantas por nombre científico o común"""
    try:
        search_term = request.args.get('q', '').strip()
        
        connection = get_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
            
        cursor = connection.cursor(dictionary=True)
        
        if search_term:
            # Búsqueda con filtro
            query = """
            SELECT DISTINCT 
                p.idPlanta,
                p.nombreCientifico,
                fp.nomFamilia,
                GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') as nombres_comunes
            FROM plantas p
            LEFT JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
            LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
            WHERE p.nombreCientifico LIKE %s 
               OR nc.nombreComun LIKE %s
            GROUP BY p.idPlanta, p.nombreCientifico, fp.nomFamilia
            ORDER BY p.nombreCientifico
            LIMIT 20
            """
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
        else:
            # Sin filtro, mostrar todas las plantas
            query = """
            SELECT DISTINCT 
                p.idPlanta,
                p.nombreCientifico,
                fp.nomFamilia,
                GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') as nombres_comunes
            FROM plantas p
            LEFT JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
            LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
            GROUP BY p.idPlanta, p.nombreCientifico, fp.nomFamilia
            ORDER BY p.nombreCientifico
            LIMIT 50
            """
            cursor.execute(query)
        
        plantas = cursor.fetchall()
        
        # Formatear los datos
        for planta in plantas:
            if not planta['nombres_comunes']:
                planta['nombres_comunes'] = 'Sin nombres comunes registrados'
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'plantas': plantas,
            'total': len(plantas)
        })
        
    except Error as e:
        print(f"Error en búsqueda de plantas: {e}")
        return jsonify({'error': 'Error al buscar plantas'}), 500

@registro_zona.route('/obtener_regiones')
def obtener_regiones():
    """Obtiene todas las regiones disponibles"""
    try:
        connection = get_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
            
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT idRegion, region FROM regiones ORDER BY region"
        cursor.execute(query)
        
        regiones = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'regiones': regiones
        })
        
    except Error as e:
        print(f"Error al obtener regiones: {e}")
        return jsonify({'error': 'Error al obtener regiones'}), 500

@registro_zona.route('/obtener_info_planta/<int:planta_id>')
def obtener_info_planta(planta_id):
    """Obtiene información detallada de una planta específica"""
    try:
        connection = get_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
            
        cursor = connection.cursor(dictionary=True)
        
        # Información básica de la planta
        query = """
        SELECT 
            p.idPlanta,
            p.nombreCientifico,
            fp.nomFamilia,
            GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') as nombres_comunes
        FROM plantas p
        LEFT JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        WHERE p.idPlanta = %s
        GROUP BY p.idPlanta, p.nombreCientifico, fp.nomFamilia
        """
        cursor.execute(query, (planta_id,))
        planta = cursor.fetchone()
        
        if not planta:
            return jsonify({'error': 'Planta no encontrada'}), 404
        
        # Obtener zonas ya registradas para esta planta
        query_zonas = """
        SELECT DISTINCT 
            r.region,
            e.ecoregion,
            nc.nombreComun
        FROM ecoregiones e
        JOIN region_ecoregion re ON e.idecoregion = re.fk_ecoregiones
        JOIN regiones r ON re.fk_regiones = r.idRegion
        LEFT JOIN nombres_comunes nc ON e.fk_plantas = nc.fk_plantas
        LEFT JOIN ubicaciones_nombres un ON nc.idNombrecomun = un.fk_nombres_comunes 
            AND un.fk_regiones = r.idRegion
        WHERE e.fk_plantas = %s
        ORDER BY r.region, e.ecoregion
        """
        cursor.execute(query_zonas, (planta_id,))
        zonas_existentes = cursor.fetchall()
        
        planta['zonas_existentes'] = zonas_existentes
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'planta': planta
        })
        
    except Error as e:
        print(f"Error al obtener info de planta: {e}")
        return jsonify({'error': 'Error al obtener información de la planta'}), 500

@registro_zona.route('/guardar_zona', methods=['POST'])
def guardar_zona():
    """Guarda una nueva zona para una planta"""
    try:
        data = request.get_json()
        
        planta_id = data.get('planta_id')
        region_id = data.get('region_id')
        ecoregion = data.get('ecoregion', '').strip()
        nombre_common = data.get('nombre_comun', '').strip()
        
        # Validaciones
        if not planta_id or not region_id or not ecoregion:
            return jsonify({'error': 'Faltan datos obligatorios'}), 400
        
        connection = get_connection()
        if not connection:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
        cursor = connection.cursor()
        
        # Iniciar transacción
        connection.start_transaction()
        
        try:
            # 1. Insertar o verificar ecoregión
            cursor.execute("""
                SELECT idecoregion FROM ecoregiones 
                WHERE fk_plantas = %s AND ecoregion = %s
            """, (planta_id, ecoregion))
            
            ecoregion_row = cursor.fetchone()
            
            if ecoregion_row:
                ecoregion_id = ecoregion_row[0]
            else:
                # Insertar nueva ecoregión
                cursor.execute("""
                    INSERT INTO ecoregiones (ecoregion, fk_plantas) 
                    VALUES (%s, %s)
                """, (ecoregion, planta_id))
                ecoregion_id = cursor.lastrowid
            
            # 2. Verificar si ya existe la relación región-ecoregión
            cursor.execute("""
                SELECT 1 FROM region_ecoregion 
                WHERE fk_ecoregiones = %s AND fk_regiones = %s
            """, (ecoregion_id, region_id))
            
            if not cursor.fetchone():
                # Insertar relación región-ecoregión
                cursor.execute("""
                    INSERT INTO region_ecoregion (fk_ecoregiones, fk_regiones) 
                    VALUES (%s, %s)
                """, (ecoregion_id, region_id))
            
            # 3. Si hay nombre común, procesarlo
            nombre_comun_id = None
            if nombre_common:
                # Verificar si ya existe este nombre común para la planta
                cursor.execute("""
                    SELECT idNombrecomun FROM nombres_comunes 
                    WHERE fk_plantas = %s AND nombreComun = %s
                """, (planta_id, nombre_common))
                
                nombre_row = cursor.fetchone()
                
                if nombre_row:
                    nombre_comun_id = nombre_row[0]
                else:
                    # Insertar nuevo nombre común
                    cursor.execute("""
                        INSERT INTO nombres_comunes (nombreComun, fk_plantas) 
                        VALUES (%s, %s)
                    """, (nombre_common, planta_id))
                    nombre_comun_id = cursor.lastrowid
                
                # Verificar y crear relación ubicación-nombre
                cursor.execute("""
                    SELECT 1 FROM ubicaciones_nombres 
                    WHERE fk_nombres_comunes = %s AND fk_regiones = %s
                """, (nombre_comun_id, region_id))
                
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO ubicaciones_nombres (fk_nombres_comunes, fk_regiones) 
                        VALUES (%s, %s)
                    """, (nombre_comun_id, region_id))
            
            # Confirmar transacción
            connection.commit()
            
            cursor.close()
            connection.close()
            
            return jsonify({
                'success': True,
                'message': 'Zona agregada exitosamente'
            })
            
        except Exception as e:
            # Revertir transacción en caso de error
            connection.rollback()
            raise e
            
    except Error as e:
        print(f"Error al guardar zona: {e}")
        return jsonify({'error': 'Error al guardar la zona'}), 500
    except Exception as e:
        print(f"Error general: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500