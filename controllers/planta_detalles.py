from flask import Blueprint, jsonify, render_template
from config.db import get_connection

detalles_bp = Blueprint('detalles_bp', __name__)

@detalles_bp.route('/detalles/<int:plant_id>')
def detalles_planta(plant_id):
    return render_template('detalleplanta.html', plant_idg=plant_id)

@detalles_bp.route('/api/planta/<int:plant_id>')
def obtener_detalles_planta(plant_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """SELECT 
            -- Información básica de la planta
            p.idPlanta,
            p.nombreCientifico,
            p.linkImagen,
            fp.nomFamilia,
            GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') AS nombres_comunes,
            
            -- Información de ecoregiones activas
            GROUP_CONCAT(DISTINCT eco.ecoregion SEPARATOR ', ') AS ecoregiones,
            
            -- Información de usos activos
            GROUP_CONCAT(DISTINCT CONCAT(u.parte, ': ', u.uso, ' (', u.preparacion, ')') SEPARATOR ' | ') AS usos_medicinales,
            
            -- Información de saberes culturales activos
            GROUP_CONCAT(DISTINCT sc.descripcionSaber SEPARATOR ' | ') AS saberes_culturales,
            
            -- Información de expertos que aportaron
            GROUP_CONCAT(DISTINCT CONCAT(pe.nombres, ' ', pe.apellido1, ' - ', ta.nombreTipo) SEPARATOR ' | ') AS aportes_expertos,
            
            -- Empleado que registró
            CONCAT(pem.nombres, ' ', pem.apellido1) AS empleado_registro,
            c.categoria AS cargo_empleado
        FROM plantas p
        INNER JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        LEFT JOIN ecoregiones eco ON p.idPlanta = eco.fk_plantas
        LEFT JOIN usos u ON p.idPlanta = u.fk_plantas AND u.idUsos NOT IN (
            SELECT DISTINCT fk_usos FROM archivaciones_usos
        )
        LEFT JOIN saberes_culturales sc ON p.idPlanta = sc.fk_plantas AND sc.idSaberes NOT IN (
            SELECT DISTINCT fk_saberes_culturales FROM archivaciones_saberes
        )
        LEFT JOIN aportes_expertos ae ON p.idPlanta = ae.fk_plantas
        LEFT JOIN personas pe ON ae.fk_personas = pe.idPersona
        LEFT JOIN tipos_aportes ta ON ae.fk_tipos_aportes = ta.idTipoAporte
        LEFT JOIN plantas_registros pr ON p.idPlanta = pr.fk_plantas
        LEFT JOIN empleados e ON pr.fk_empleados = e.idEmpleado
        LEFT JOIN personas pem ON e.fk_personas = pem.idPersona
        LEFT JOIN cargos c ON e.fk_cargos = c.idCargo
        WHERE p.idPlanta = %s AND p.idPlanta NOT IN (
            SELECT DISTINCT fk_plantas FROM archivacionesplantas
        )
        GROUP BY p.idPlanta, p.nombreCientifico, p.linkImagen, fp.nomFamilia, 
                 pem.nombres, pem.apellido1, c.categoria"""
        cursor.execute(query, (plant_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({'error': 'Planta no encontrada'}), 404

        resultado = {
            'idPlanta': row[0],
            'nombreCientifico': row[1],
            'linkImagen': row[2],
            'nomFamilia': row[3],
            'nombres_comunes': row[4],
            'ecoregiones': row[5],
            'usos_medicinales': row[6],
            'saberes_culturales': row[7],
            'aportes_expertos': row[8],
            'empleado_registro': row[9],
            'cargo_empleado': row[10]
        }

        return jsonify(resultado)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
