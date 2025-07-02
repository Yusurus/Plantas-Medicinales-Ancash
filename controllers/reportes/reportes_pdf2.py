from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from config.db import get_connection
import mysql.connector
from datetime import datetime

reporte_bp = Blueprint('reporte', __name__)

class PlantasController:
    """Controlador para manejar reportes de plantas medicinales"""
    
    @staticmethod
    def obtener_informacion_basica_planta(id_planta):
        """Obtiene información básica de la planta: nombre científico, familia, nombres comunes"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT 
                p.idPlanta,
                p.nombreCientifico,
                fp.nomFamilia,
                GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') AS nombres_comunes
            FROM plantas p
            INNER JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
            LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
            WHERE p.idPlanta = %s
            GROUP BY p.idPlanta, p.nombreCientifico, fp.nomFamilia
            """
            cursor.execute(query, (id_planta,))
            return cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Error al obtener información básica: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def obtener_datos_morfologicos(id_planta):
        """Obtiene datos morfológicos de la planta"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT 
                dm.idDatomorfologico,
                dm.datoMorfologico
            FROM datos_morfologicos dm
            WHERE dm.fk_plantas = %s
            ORDER BY dm.idDatomorfologico
            """
            cursor.execute(query, (id_planta,))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al obtener datos morfológicos: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def obtener_imagenes(id_planta):
        """Obtiene enlaces de imágenes de la planta"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT 
                li.idLinksImagenes,
                li.linkImagen
            FROM linksimagenes li
            WHERE li.fk_plantas = %s
            ORDER BY li.idLinksImagenes
            """
            cursor.execute(query, (id_planta,))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al obtener imágenes: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def obtener_ubicaciones_geograficas(id_planta):
        """Obtiene información de ubicaciones geográficas"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT DISTINCT
                eco.ecoregion,
                prov.nombreProvincia,
                reg.region
            FROM ecoregion_planta ep
            INNER JOIN ecoregiones eco ON ep.fk_ecoregiones = eco.idecoregion
            LEFT JOIN provincia_ecoregion pe ON eco.idecoregion = pe.fk_ecoregiones
            LEFT JOIN provincias prov ON pe.fk_provincias = prov.idprovincias
            LEFT JOIN regiones reg ON prov.fk_regiones = reg.idRegion
            WHERE ep.fk_plantas = %s
            ORDER BY reg.region, prov.nombreProvincia, eco.ecoregion
            """
            cursor.execute(query, (id_planta,))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al obtener ubicaciones: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def obtener_usos_medicinales(id_planta):
        """Obtiene información de usos medicinales"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT 
                u.idUsos,
                u.parte,
                u.uso,
                u.preparacion,
                u.contraIndicaciones
            FROM usos u
            WHERE u.fk_plantas = %s
            ORDER BY u.parte, u.uso
            """
            cursor.execute(query, (id_planta,))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al obtener usos medicinales: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def obtener_saberes_culturales(id_planta):
        """Obtiene saberes culturales de la planta"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT 
                sc.idSaberes,
                sc.descripcionSaber
            FROM saberes_culturales sc
            WHERE sc.fk_plantas = %s
            ORDER BY sc.idSaberes
            """
            cursor.execute(query, (id_planta,))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al obtener saberes culturales: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def obtener_aportes_expertos(id_planta):
        """Obtiene aportes de expertos"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT 
                ae.idAporteExperto,
                ae.fecha,
                ae.descripcion,
                CONCAT(p.nombres, ' ', p.apellido1, ' ', p.apellido2) AS nombre_experto,
                p.DNI,
                p.telefono,
                ta.nombreTipo AS tipo_aporte
            FROM aportes_expertos ae
            INNER JOIN personas p ON ae.fk_personas = p.idPersona
            INNER JOIN tipos_aportes ta ON ae.fk_tipos_aportes = ta.idTipoAporte
            WHERE ae.fk_plantas = %s
            ORDER BY ae.fecha DESC, ae.idAporteExperto
            """
            cursor.execute(query, (id_planta,))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al obtener aportes de expertos: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def obtener_empleados_registro(id_planta):
        """Obtiene información de empleados que registraron la planta"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT DISTINCT
                CONCAT(p.nombres, ' ', p.apellido1, ' ', p.apellido2) AS nombre_empleado,
                p.DNI,
                e.correo,
                c.categoria AS cargo
            FROM plantas_registros pr
            INNER JOIN empleados e ON pr.fk_empleados = e.idEmpleado
            INNER JOIN personas p ON e.fk_personas = p.idPersona
            INNER JOIN cargos c ON e.fk_cargos = c.idCargo
            WHERE pr.fk_plantas = %s
            """
            cursor.execute(query, (id_planta,))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al obtener empleados de registro: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def obtener_historial_archivaciones(id_planta):
        """Obtiene historial de archivaciones de la planta"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            # Archivaciones de la planta
            query_planta = """
            SELECT 
                ap.idArchivaPlanta,
                ap.fecha,
                ap.motivo,
                CONCAT(p.nombres, ' ', p.apellido1, ' ', p.apellido2) AS empleado_archivo,
                e.correo,
                c.categoria AS cargo_empleado,
                'PLANTA' as tipo_archivacion
            FROM archivacionesplantas ap
            INNER JOIN empleados e ON ap.fk_empleados = e.idEmpleado
            INNER JOIN personas p ON e.fk_personas = p.idPersona
            INNER JOIN cargos c ON e.fk_cargos = c.idCargo
            WHERE ap.fk_plantas = %s
            ORDER BY ap.fecha DESC
            """
            
            # Archivaciones de usos
            query_usos = """
            SELECT 
                au.idArchivaUso as id_archivacion,
                au.fecha,
                au.motivo,
                CONCAT(p.nombres, ' ', p.apellido1, ' ', p.apellido2) AS empleado_archivo,
                CONCAT('Uso: ', u.parte, ' - ', u.uso) as detalle_archivado,
                'USO' as tipo_archivacion
            FROM archivaciones_usos au
            INNER JOIN usos u ON au.fk_usos = u.idUsos
            INNER JOIN empleados e ON au.fk_empleados = e.idEmpleado
            INNER JOIN personas p ON e.fk_personas = p.idPersona
            WHERE u.fk_plantas = %s
            ORDER BY au.fecha DESC
            """
            
            # Archivaciones de saberes
            query_saberes = """
            SELECT 
                asab.idArchivaSaber as id_archivacion,
                asab.fechaArchivaSaber as fecha,
                asab.motivoArchivaSaber as motivo,
                CONCAT(p.nombres, ' ', p.apellido1, ' ', p.apellido2) AS empleado_archivo,
                CONCAT('Saber: ', LEFT(sc.descripcionSaber, 50), '...') as detalle_archivado,
                'SABER' as tipo_archivacion
            FROM archivaciones_saberes asab
            INNER JOIN saberes_culturales sc ON asab.fk_saberes_culturales = sc.idSaberes
            INNER JOIN empleados e ON asab.fk_empleados = e.idEmpleado
            INNER JOIN personas p ON e.fk_personas = p.idPersona
            WHERE sc.fk_plantas = %s
            ORDER BY asab.fechaArchivaSaber DESC
            """
            
            cursor = connection.cursor(dictionary=True)
            
            # Ejecutar todas las consultas
            cursor.execute(query_planta, (id_planta,))
            archivaciones_planta = cursor.fetchall()
            
            cursor.execute(query_usos, (id_planta,))
            archivaciones_usos = cursor.fetchall()
            
            cursor.execute(query_saberes, (id_planta,))
            archivaciones_saberes = cursor.fetchall()
            
            # Combinar todos los resultados
            todas_archivaciones = archivaciones_planta + archivaciones_usos + archivaciones_saberes
            
            # Ordenar por fecha
            todas_archivaciones.sort(key=lambda x: x['fecha'], reverse=True)
            
            return todas_archivaciones
            
        except mysql.connector.Error as e:
            print(f"Error al obtener historial de archivaciones: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def obtener_reporte_completo_planta(id_planta):
        """Obtiene toda la información de una planta específica"""
        try:
            # Obtener todos los datos
            info_basica = PlantasController.obtener_informacion_basica_planta(id_planta)
            if not info_basica:
                return None
                
            datos = {
                'info_basica': info_basica,
                'datos_morfologicos': PlantasController.obtener_datos_morfologicos(id_planta),
                'imagenes': PlantasController.obtener_imagenes(id_planta),
                'ubicaciones': PlantasController.obtener_ubicaciones_geograficas(id_planta),
                'usos_medicinales': PlantasController.obtener_usos_medicinales(id_planta),
                'saberes_culturales': PlantasController.obtener_saberes_culturales(id_planta),
                'aportes_expertos': PlantasController.obtener_aportes_expertos(id_planta),
                'empleados_registro': PlantasController.obtener_empleados_registro(id_planta),
                'historial_archivaciones': PlantasController.obtener_historial_archivaciones(id_planta)
            }
            
            return datos
            
        except Exception as e:
            print(f"Error al obtener reporte completo: {e}")
            return None

    @staticmethod
    def obtener_lista_plantas():
        """Obtiene lista resumida de todas las plantas para selección"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT 
                p.idPlanta,
                p.nombreCientifico,
                fp.nomFamilia,
                GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') AS nombres_comunes,
                COUNT(DISTINCT u.idUsos) as total_usos,
                COUNT(DISTINCT sc.idSaberes) as total_saberes,
                CASE 
                    WHEN EXISTS(SELECT 1 FROM archivacionesplantas ap WHERE ap.fk_plantas = p.idPlanta)
                    THEN 'ARCHIVADA'
                    ELSE 'ACTIVA'
                END AS estado
            FROM plantas p
            INNER JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
            LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
            LEFT JOIN usos u ON p.idPlanta = u.fk_plantas
            LEFT JOIN saberes_culturales sc ON p.idPlanta = sc.fk_plantas
            GROUP BY p.idPlanta, p.nombreCientifico, fp.nomFamilia
            ORDER BY p.nombreCientifico
            """
            cursor.execute(query)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"Error al obtener lista de plantas: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

# Rutas del Blueprint
@reporte_bp.route('/plantas')
def lista_plantas():
    """Muestra la lista de plantas disponibles"""
    if 'usuario' not in session:
        return redirect(url_for('user.login'))
    
    plantas = PlantasController.obtener_lista_plantas()
    return render_template('reportes/lista_plantas.html', plantas=plantas)

@reporte_bp.route('/planta/<int:id_planta>')
def detalle_planta(id_planta):
    """Muestra el reporte completo de una planta específica"""
    if 'usuario' not in session:
        return redirect(url_for('user.login'))
    
    datos_planta = PlantasController.obtener_reporte_completo_planta(id_planta)
    
    if not datos_planta:
        return render_template('error.html', mensaje="Planta no encontrada"), 404
    
    return render_template('reportes/detalle_planta.html', 
                         datos=datos_planta,
                         fecha_generacion=datetime.now().strftime("%d/%m/%Y %H:%M"))

@reporte_bp.route('/api/planta/<int:id_planta>')
def api_detalle_planta(id_planta):
    """API para obtener datos de una planta en formato JSON"""
    if 'usuario' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    datos_planta = PlantasController.obtener_reporte_completo_planta(id_planta)
    
    if not datos_planta:
        return jsonify({'error': 'Planta no encontrada'}), 404
    
    # Convertir datetime a string para JSON
    for aporte in datos_planta.get('aportes_expertos', []):
        if aporte.get('fecha'):
            aporte['fecha'] = aporte['fecha'].strftime("%d/%m/%Y")
    
    for archivacion in datos_planta.get('historial_archivaciones', []):
        if archivacion.get('fecha'):
            archivacion['fecha'] = archivacion['fecha'].strftime("%d/%m/%Y")
    
    return jsonify(datos_planta)

@reporte_bp.route('/buscar_plantas')
def buscar_plantas():
    """Busca plantas por nombre científico o común"""
    if 'usuario' not in session:
        return redirect(url_for('user.login'))
    
    termino_busqueda = request.args.get('q', '').strip()
    
    if not termino_busqueda:
        return jsonify([])
    
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = """
        SELECT DISTINCT
            p.idPlanta,
            p.nombreCientifico,
            fp.nomFamilia,
            GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') AS nombres_comunes
        FROM plantas p
        INNER JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        WHERE p.nombreCientifico LIKE %s 
           OR nc.nombreComun LIKE %s
           OR fp.nomFamilia LIKE %s
        GROUP BY p.idPlanta, p.nombreCientifico, fp.nomFamilia
        ORDER BY p.nombreCientifico
        LIMIT 10
        """
        
        termino_like = f"%{termino_busqueda}%"
        cursor.execute(query, (termino_like, termino_like, termino_like))
        resultados = cursor.fetchall()
        
        return jsonify(resultados)
        
    except mysql.connector.Error as e:
        print(f"Error en búsqueda: {e}")
        return jsonify([])
    finally:
        cursor.close()
        connection.close()