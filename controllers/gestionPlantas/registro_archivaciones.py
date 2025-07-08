from flask import request, jsonify, Blueprint, session
from config.db import get_connection
from datetime import datetime

registro_archivaciones = Blueprint("registro_archivaciones", __name__)

def get_empleado_id():
    empleado_id = session.get("usuario")
    if not empleado_id:
        return None
    return empleado_id.get("idEmpleado")

# --------------------------- PLANTAS ---------------------------
@registro_archivaciones.route('/api/plantas_activas', methods=['GET'])
def get_plantas_activas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            p.idPlanta,
            p.nombreCientifico,
            fp.nomFamilia,
            (SELECT li.linkImagen FROM linksimagenes li WHERE li.fk_plantas = p.idPlanta LIMIT 1) AS linkImagen,
            GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') AS nombres_comunes
        FROM plantas p
        JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        WHERE p.idPlanta NOT IN (SELECT fk_plantas FROM archivacionesplantas)
        GROUP BY p.idPlanta
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@registro_archivaciones.route('/api/plantas_archivadas', methods=['GET'])
def get_plantas_archivadas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            p.idPlanta,
            p.nombreCientifico,
            fp.nomFamilia,
            (SELECT li.linkImagen FROM linksimagenes li WHERE li.fk_plantas = p.idPlanta LIMIT 1) AS linkImagen,
            GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') AS nombres_comunes
        FROM plantas p
        JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        WHERE p.idPlanta IN (SELECT fk_plantas FROM archivacionesplantas)
        GROUP BY p.idPlanta
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@registro_archivaciones.route('/api/archive_plant/<int:plant_id>', methods=['PUT'])
def archive_plant(plant_id):
    motivo = request.json.get("motivo", "Sin motivo especificado")
    fk_empleado = get_empleado_id()
    if not fk_empleado:
        return jsonify({'error': 'Sesión no válida'}), 401

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM archivacionesplantas WHERE fk_plantas = %s", (plant_id,))
    if cursor.fetchone():
        return jsonify({'error': 'La planta ya está archivada'}), 400

    cursor.execute("""
        INSERT INTO archivacionesplantas (fecha, motivo, fk_plantas, fk_empleados)
        VALUES (%s, %s, %s, %s)
    """, (datetime.today(), motivo, plant_id, fk_empleado))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

# --------------------------- ZONAS ---------------------------
@registro_archivaciones.route('/api/zonas_activas', methods=['GET'])
def get_zonas_activas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            ep.idecoregion_planta AS idZona,
            e.ecoregion,
            GROUP_CONCAT(DISTINCT prov.nombreProvincia) AS nombreProvincia,
            GROUP_CONCAT(DISTINCT r.region) AS region
        FROM ecoregion_planta ep
        JOIN ecoregiones e ON ep.fk_ecoregiones = e.idecoregion
        LEFT JOIN provincia_ecoregion pe ON pe.fk_ecoregiones = e.idecoregion
        LEFT JOIN provincias prov ON pe.fk_provincias = prov.idprovincias
        LEFT JOIN regiones r ON prov.fk_regiones = r.idRegion
        WHERE ep.idecoregion_planta NOT IN (
            SELECT fk_ecoregion_plantas FROM archivaciones_ubicaciones
        )
        GROUP BY ep.idecoregion_planta, e.ecoregion
    """)
    zonas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(zonas)

@registro_archivaciones.route('/api/zonas_archivadas', methods=['GET'])
def get_zonas_archivadas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            ep.idecoregion_planta AS idZona,
            e.ecoregion,
            GROUP_CONCAT(DISTINCT prov.nombreProvincia) AS nombreProvincia,
            GROUP_CONCAT(DISTINCT r.region) AS region
        FROM ecoregion_planta ep
        JOIN ecoregiones e ON ep.fk_ecoregiones = e.idecoregion
        LEFT JOIN provincia_ecoregion pe ON pe.fk_ecoregiones = e.idecoregion
        LEFT JOIN provincias prov ON pe.fk_provincias = prov.idprovincias
        LEFT JOIN regiones r ON prov.fk_regiones = r.idRegion
        WHERE ep.idecoregion_planta IN (
            SELECT fk_ecoregion_plantas FROM archivaciones_ubicaciones
        )
        GROUP BY ep.idecoregion_planta, e.ecoregion
    """)
    zonas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(zonas)

@registro_archivaciones.route('/api/archive_zona/<int:zona_id>', methods=['PUT'])
def archive_zona(zona_id):
    motivo = request.json.get("motivo", "Sin motivo especificado")
    fk_empleado = get_empleado_id()
    if not fk_empleado:
        return jsonify({'error': 'Sesión no válida'}), 401

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM archivaciones_ubicaciones WHERE fk_ecoregion_plantas = %s", (zona_id,))
    if cursor.fetchone():
        return jsonify({'error': 'La zona ya está archivada'}), 400

    cursor.execute("""
        INSERT INTO archivaciones_ubicaciones (fecha, motivo, fk_ecoregion_plantas, fk_idempleados)
        VALUES (%s, %s, %s, %s)
    """, (datetime.today(), motivo, zona_id, fk_empleado))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

# --------------------------- SABERES CULTURALES ---------------------------
@registro_archivaciones.route('/api/saberes_culturales_activos', methods=['GET'])
def get_saberes_activos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT sc.idSaberes AS idSaberesCulturales, sc.descripcionSaber, p.nombreCientifico
        FROM saberes_culturales sc
        JOIN plantas p ON sc.fk_plantas = p.idPlanta
        WHERE sc.idSaberes NOT IN (
            SELECT fk_saberes_culturales FROM archivaciones_saberes
        )
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@registro_archivaciones.route('/api/saberes_culturales_archivados', methods=['GET'])
def get_saberes_archivados():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT sc.idSaberes AS idSaberesCulturales, sc.descripcionSaber, p.nombreCientifico
        FROM saberes_culturales sc
        JOIN plantas p ON sc.fk_plantas = p.idPlanta
        WHERE sc.idSaberes IN (
            SELECT fk_saberes_culturales FROM archivaciones_saberes
        )
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@registro_archivaciones.route('/api/archive_saber/<int:saber_id>', methods=['PUT'])
def archive_saber(saber_id):
    motivo = request.json.get("motivo", "Sin motivo especificado")
    fk_empleado = get_empleado_id()
    if not fk_empleado:
        return jsonify({'error': 'Sesión no válida'}), 401

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM archivaciones_saberes WHERE fk_saberes_culturales = %s", (saber_id,))
    if cursor.fetchone():
        return jsonify({'error': 'El saber ya está archivado'}), 400

    cursor.execute("""
        INSERT INTO archivaciones_saberes (fechaArchivaSaber, motivoArchivaSaber, fk_saberes_culturales, fk_empleados)
        VALUES (%s, %s, %s, %s)
    """, (datetime.today(), motivo, saber_id, fk_empleado))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

# --------------------------- USOS MEDICINALES ---------------------------
@registro_archivaciones.route('/api/usos_medicinales_activos', methods=['GET'])
def get_usos_activos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.idUsos, u.uso, u.parte, u.preparacion, p.nombreCientifico
        FROM usos u
        JOIN plantas p ON u.fk_plantas = p.idPlanta
        WHERE u.idUsos NOT IN (
            SELECT fk_usos FROM archivaciones_usos
        )
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@registro_archivaciones.route('/api/usos_medicinales_archivados', methods=['GET'])
def get_usos_archivados():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.idUsos, u.uso, u.parte, u.preparacion, p.nombreCientifico
        FROM usos u
        JOIN plantas p ON u.fk_plantas = p.idPlanta
        WHERE u.idUsos IN (
            SELECT fk_usos FROM archivaciones_usos
        )
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@registro_archivaciones.route('/api/archive_uso/<int:uso_id>', methods=['PUT'])
def archive_uso(uso_id):
    motivo = request.json.get("motivo", "Sin motivo especificado")
    fk_empleado = get_empleado_id()
    if not fk_empleado:
        return jsonify({'error': 'Sesión no válida'}), 401

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM archivaciones_usos WHERE fk_usos = %s", (uso_id,))
    if cursor.fetchone():
        return jsonify({'error': 'El uso ya está archivado'}), 400

    cursor.execute("""
        INSERT INTO archivaciones_usos (fecha, motivo, fk_usos, fk_empleados)
        VALUES (%s, %s, %s, %s)
    """, (datetime.today(), motivo, uso_id, fk_empleado))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})
