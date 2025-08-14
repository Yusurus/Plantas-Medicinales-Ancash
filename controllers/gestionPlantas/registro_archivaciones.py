from flask import Blueprint, request, jsonify, session
from config.db import get_connection
from datetime import datetime

registro_archivaciones = Blueprint("registro_archivaciones", __name__)

def get_empleado_id():
    user = session.get("usuario")
    if not user:
        return None
    return user.get("idEmpleado")

# --------------------------- PLANTAS ---------------------------
@registro_archivaciones.route('/api/plantas_activas', methods=['GET'])
def get_plantas_activas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.idPlanta, p.nombreCientifico, fp.nomFamilia,
               GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') AS nombres_comunes
        FROM plantas p
        JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON nc.fk_plantas = p.idPlanta
        WHERE p.idPlanta NOT IN (SELECT fk_plantas FROM archivacionesplantas)
        GROUP BY p.idPlanta
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

@registro_archivaciones.route('/api/plantas/<int:id>/detalles', methods=['GET'])
def get_detalles_planta(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ep.idecoregion_planta AS idZona, e.ecoregion
        FROM ecoregion_planta ep
        JOIN ecoregiones e ON ep.fk_ecoregiones = e.idecoregion
        WHERE ep.fk_plantas = %s
          AND ep.idecoregion_planta NOT IN (SELECT fk_ecoregion_plantas FROM archivaciones_ubicaciones)
    """, (id,))
    zonas = cursor.fetchall()

    cursor.execute("""
        SELECT sc.idSaberes AS idSaberesCulturales, sc.descripcionSaber
        FROM saberes_culturales sc
        WHERE sc.fk_plantas = %s
          AND sc.idSaberes NOT IN (SELECT fk_saberes_culturales FROM archivaciones_saberes)
    """, (id,))
    saberes = cursor.fetchall()

    cursor.execute("""
        SELECT u.idUsos, u.uso, u.parte, u.preparacion
        FROM usos u
        WHERE u.fk_plantas = %s
          AND u.idUsos NOT IN (SELECT fk_usos FROM archivaciones_usos)
    """, (id,))
    usos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"zonas": zonas, "saberes": saberes, "usos": usos})

@registro_archivaciones.route('/api/plantas/<int:id>/archivados', methods=['GET'])
def get_detalles_archivados(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ep.idecoregion_planta AS idZona, e.ecoregion
        FROM ecoregion_planta ep
        JOIN ecoregiones e ON ep.fk_ecoregiones = e.idecoregion
        WHERE ep.fk_plantas = %s
          AND ep.idecoregion_planta IN (SELECT fk_ecoregion_plantas FROM archivaciones_ubicaciones)
    """, (id,))
    zonas = cursor.fetchall()

    cursor.execute("""
        SELECT sc.idSaberes AS idSaberesCulturales, sc.descripcionSaber
        FROM saberes_culturales sc
        WHERE sc.fk_plantas = %s
          AND sc.idSaberes IN (SELECT fk_saberes_culturales FROM archivaciones_saberes)
    """, (id,))
    saberes = cursor.fetchall()

    cursor.execute("""
        SELECT u.idUsos, u.uso, u.parte, u.preparacion
        FROM usos u
        WHERE u.fk_plantas = %s
          AND u.idUsos IN (SELECT fk_usos FROM archivaciones_usos)
    """, (id,))
    usos = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify({"zonas": zonas, "saberes": saberes, "usos": usos})

# --------------------------- ARCHIVACIONES ---------------------------
@registro_archivaciones.route('/api/archive_plant/<int:plant_id>', methods=['PUT'])
def archive_plant(plant_id):
    data = request.get_json()
    motivo = data.get("motivo", "Sin motivo")
    empleado = get_empleado_id()
    if not empleado:
        return jsonify({"error": "Sesión no válida"}), 401

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT 1 FROM archivacionesplantas WHERE fk_plantas = %s", (plant_id,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "Ya archivado"})

    cursor.execute("""
        INSERT INTO archivacionesplantas (fecha, motivo, fk_plantas, fk_empleados)
        VALUES (%s, %s, %s, %s)
    """, (datetime.today(), motivo, plant_id, empleado))

    cursor.execute("""
        SELECT idecoregion_planta FROM ecoregion_planta
        WHERE fk_plantas = %s
          AND idecoregion_planta NOT IN (SELECT fk_ecoregion_plantas FROM archivaciones_ubicaciones)
    """, (plant_id,))
    zonas = cursor.fetchall()
    for z in zonas:
        cursor.execute("""
            INSERT INTO archivaciones_ubicaciones (fecha, motivo, fk_ecoregion_plantas, fk_idempleados)
            VALUES (%s, %s, %s, %s)
        """, (datetime.today(), motivo, z['idecoregion_planta'], empleado))

    cursor.execute("""
        SELECT idSaberes FROM saberes_culturales
        WHERE fk_plantas = %s
          AND idSaberes NOT IN (SELECT fk_saberes_culturales FROM archivaciones_saberes)
    """, (plant_id,))
    saberes = cursor.fetchall()
    for s in saberes:
        cursor.execute("""
            INSERT INTO archivaciones_saberes (fechaArchivaSaber, motivoArchivaSaber, fk_saberes_culturales, fk_empleados)
            VALUES (%s, %s, %s, %s)
        """, (datetime.today(), motivo, s['idSaberes'], empleado))

    cursor.execute("""
        SELECT idUsos FROM usos
        WHERE fk_plantas = %s
          AND idUsos NOT IN (SELECT fk_usos FROM archivaciones_usos)
    """, (plant_id,))
    usos = cursor.fetchall()
    for u in usos:
        cursor.execute("""
            INSERT INTO archivaciones_usos (fecha, motivo, fk_usos, fk_empleados)
            VALUES (%s, %s, %s, %s)
        """, (datetime.today(), motivo, u['idUsos'], empleado))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True})

@registro_archivaciones.route('/api/archive_zona/<int:zona_id>', methods=['PUT'])
def archive_zona(zona_id):
    data = request.get_json()
    motivo = data.get("motivo", "Sin motivo")
    empleado = get_empleado_id()
    if not empleado:
        return jsonify({"error": "Sesión no válida"}), 401

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM archivaciones_ubicaciones WHERE fk_ecoregion_plantas = %s", (zona_id,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "Ya archivado"})

    cursor.execute("""
        INSERT INTO archivaciones_ubicaciones (fecha, motivo, fk_ecoregion_plantas, fk_idempleados)
        VALUES (%s, %s, %s, %s)
    """, (datetime.today(), motivo, zona_id, empleado))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True})

@registro_archivaciones.route('/api/archive_saber/<int:saber_id>', methods=['PUT'])
def archive_saber(saber_id):
    data = request.get_json()
    motivo = data.get("motivo", "Sin motivo")
    empleado = get_empleado_id()
    if not empleado:
        return jsonify({"error": "Sesión no válida"}), 401

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM archivaciones_saberes WHERE fk_saberes_culturales = %s", (saber_id,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "Ya archivado"})

    cursor.execute("""
        INSERT INTO archivaciones_saberes (fechaArchivaSaber, motivoArchivaSaber, fk_saberes_culturales, fk_empleados)
        VALUES (%s, %s, %s, %s)
    """, (datetime.today(), motivo, saber_id, empleado))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True})

@registro_archivaciones.route('/api/archive_uso/<int:uso_id>', methods=['PUT'])
def archive_uso(uso_id):
    data = request.get_json()
    motivo = data.get("motivo", "Sin motivo")
    empleado = get_empleado_id()
    if not empleado:
        return jsonify({"error": "Sesión no válida"}), 401

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM archivaciones_usos WHERE fk_usos = %s", (uso_id,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"success": False, "message": "Ya archivado"})

    cursor.execute("""
        INSERT INTO archivaciones_usos (fecha, motivo, fk_usos, fk_empleados)
        VALUES (%s, %s, %s, %s)
    """, (datetime.today(), motivo, uso_id, empleado))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"success": True})
