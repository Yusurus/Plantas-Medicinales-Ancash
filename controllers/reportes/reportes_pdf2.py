from flask import Blueprint, render_template, session, redirect, url_for, make_response, jsonify, request
from config.db import get_connection
import mysql.connector
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

reporte_bp = Blueprint('reporte', __name__)

class PlantasController:
    """Controlador para manejar operaciones relacionadas con plantas medicinales"""
    
    @staticmethod
    def obtener_informacion_basica_planta(id_planta):
        """Obtiene información básica de una planta específica"""
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
            logger.error(f"Error al obtener información básica: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def obtener_datos_morfologicos(id_planta):
        """Obtiene datos morfológicos de una planta"""
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
            logger.error(f"Error al obtener datos morfológicos: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def obtener_imagenes_planta(id_planta):
        """Obtiene todas las imágenes de una planta"""
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
            logger.error(f"Error al obtener imágenes: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def obtener_ubicaciones_geograficas(id_planta):
        """Obtiene ubicaciones geográficas de una planta"""
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
            logger.error(f"Error al obtener ubicaciones: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def obtener_usos_medicinales(id_planta):
        """Obtiene usos medicinales de una planta"""
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
            logger.error(f"Error al obtener usos medicinales: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def obtener_saberes_culturales(id_planta):
        """Obtiene saberes culturales de una planta"""
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
            logger.error(f"Error al obtener saberes culturales: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def obtener_aportes_expertos(id_planta):
        """Obtiene aportes de expertos para una planta"""
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
            logger.error(f"Error al obtener aportes de expertos: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def obtener_empleados_registro(id_planta):
        """Obtiene empleados que registraron la planta"""
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
            logger.error(f"Error al obtener empleados de registro: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def obtener_resumen_consolidado(id_planta):
        """Obtiene un resumen consolidado de toda la información de una planta"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT 
                -- Información básica
                p.idPlanta,
                p.nombreCientifico,
                fp.nomFamilia,
                
                -- Nombres comunes
                (SELECT GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ')
                 FROM nombres_comunes nc 
                 WHERE nc.fk_plantas = p.idPlanta) AS nombres_comunes,
                
                -- Datos morfológicos
                (SELECT GROUP_CONCAT(DISTINCT dm.datoMorfologico SEPARATOR ' | ')
                 FROM datos_morfologicos dm 
                 WHERE dm.fk_plantas = p.idPlanta) AS datos_morfologicos,
                
                -- Primera imagen
                (SELECT li.linkImagen 
                 FROM linksimagenes li 
                 WHERE li.fk_plantas = p.idPlanta 
                 LIMIT 1) AS imagen_principal,
                
                -- Total de imágenes
                (SELECT COUNT(*) 
                 FROM linksimagenes li 
                 WHERE li.fk_plantas = p.idPlanta) AS total_imagenes,
                
                -- Ecoregiones
                (SELECT GROUP_CONCAT(DISTINCT eco.ecoregion SEPARATOR ', ')
                 FROM ecoregion_planta ep
                 INNER JOIN ecoregiones eco ON ep.fk_ecoregiones = eco.idecoregion
                 WHERE ep.fk_plantas = p.idPlanta) AS ecoregiones,
                
                -- Total de usos
                (SELECT COUNT(*) 
                 FROM usos u 
                 WHERE u.fk_plantas = p.idPlanta) AS total_usos,
                
                -- Total de saberes culturales
                (SELECT COUNT(*) 
                 FROM saberes_culturales sc 
                 WHERE sc.fk_plantas = p.idPlanta) AS total_saberes,
                
                -- Total de aportes de expertos
                (SELECT COUNT(*) 
                 FROM aportes_expertos ae 
                 WHERE ae.fk_plantas = p.idPlanta) AS total_aportes,
                
                -- Estado de archivación
                CASE 
                    WHEN EXISTS(SELECT 1 FROM archivacionesplantas ap WHERE ap.fk_plantas = p.idPlanta)
                    THEN 'ARCHIVADA'
                    ELSE 'ACTIVA'
                END AS estado_planta
                
            FROM plantas p
            INNER JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
            WHERE p.idPlanta = %s
            """
            
            cursor.execute(query, (id_planta,))
            return cursor.fetchone()
            
        except mysql.connector.Error as e:
            logger.error(f"Error al obtener resumen consolidado: {e}")
            return None
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def obtener_reporte_completo_planta(id_planta):
        """Obtiene toda la información de una planta para reporte completo"""
        try:
            # Obtener todos los datos por separado
            informacion_basica = PlantasController.obtener_informacion_basica_planta(id_planta)
            datos_morfologicos = PlantasController.obtener_datos_morfologicos(id_planta)
            imagenes = PlantasController.obtener_imagenes_planta(id_planta)
            ubicaciones = PlantasController.obtener_ubicaciones_geograficas(id_planta)
            usos = PlantasController.obtener_usos_medicinales(id_planta)
            saberes = PlantasController.obtener_saberes_culturales(id_planta)
            aportes = PlantasController.obtener_aportes_expertos(id_planta)
            empleados = PlantasController.obtener_empleados_registro(id_planta)
            resumen = PlantasController.obtener_resumen_consolidado(id_planta)
            
            return {
                'informacion_basica': informacion_basica,
                'datos_morfologicos': datos_morfologicos,
                'imagenes': imagenes,
                'ubicaciones': ubicaciones,
                'usos_medicinales': usos,
                'saberes_culturales': saberes,
                'aportes_expertos': aportes,
                'empleados_registro': empleados,
                'resumen': resumen
            }
            
        except Exception as e:
            logger.error(f"Error al obtener reporte completo: {e}")
            return None
    
    @staticmethod
    def obtener_todas_las_plantas():
        """Obtiene un listado de todas las plantas para reportes generales"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT 
                p.idPlanta,
                p.nombreCientifico,
                fp.nomFamilia,
                GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') as nombres_comunes,
                COUNT(DISTINCT u.idUsos) as total_usos,
                COUNT(DISTINCT sc.idSaberes) as total_saberes,
                CASE 
                    WHEN EXISTS(SELECT 1 FROM archivacionesplantas ap WHERE ap.fk_plantas = p.idPlanta)
                    THEN 'ARCHIVADA'
                    ELSE 'ACTIVA'
                END AS estado
            FROM plantas p
            LEFT JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
            LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
            LEFT JOIN usos u ON p.idPlanta = u.fk_plantas
            LEFT JOIN saberes_culturales sc ON p.idPlanta = sc.fk_plantas
            GROUP BY p.idPlanta, p.nombreCientifico, fp.nomFamilia
            ORDER BY p.nombreCientifico
            """
            
            cursor.execute(query)
            return cursor.fetchall()
            
        except mysql.connector.Error as e:
            logger.error(f"Error al obtener todas las plantas: {e}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    @staticmethod
    def obtener_estadisticas_generales():
        """Obtiene estadísticas generales del sistema"""
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT 
                (SELECT COUNT(*) FROM plantas) as total_plantas,
                (SELECT COUNT(*) FROM plantas WHERE NOT EXISTS(
                    SELECT 1 FROM archivacionesplantas ap WHERE ap.fk_plantas = plantas.idPlanta
                )) as plantas_activas,
                (SELECT COUNT(*) FROM archivacionesplantas) as plantas_archivadas,
                (SELECT COUNT(*) FROM familias_plantas) as total_familias,
                (SELECT COUNT(*) FROM nombres_comunes) as total_nombres_comunes,
                (SELECT COUNT(*) FROM usos) as total_usos,
                (SELECT COUNT(*) FROM saberes_culturales) as total_saberes,
                (SELECT COUNT(*) FROM aportes_expertos) as total_aportes,
                (SELECT COUNT(*) FROM ecoregiones) as total_ecoregiones,
                (SELECT COUNT(*) FROM regiones) as total_regiones
            """
            
            cursor.execute(query)
            return cursor.fetchone()
            
        except mysql.connector.Error as e:
            logger.error(f"Error al obtener estadísticas: {e}")
            return {}
        finally:
            cursor.close()
            connection.close()

# RUTAS DEL BLUEPRINT

@reporte_bp.route('/plantas')
def listar_plantas():
    """Lista todas las plantas disponibles"""
    if 'usuario' not in session:
        return redirect(url_for('user.login'))
    
    plantas = PlantasController.obtener_todas_las_plantas()
    estadisticas = PlantasController.obtener_estadisticas_generales()
    
    return render_template('reportes/lista_plantas.html', 
                         plantas=plantas, 
                         estadisticas=estadisticas)

@reporte_bp.route('/planta/<int:id_planta>')
def detalle_planta(id_planta):
    """Muestra el detalle completo de una planta"""
    if 'usuario' not in session:
        return redirect(url_for('user.login'))
    
    datos_planta = PlantasController.obtener_reporte_completo_planta(id_planta)
    
    if not datos_planta:
        return render_template('error.html', 
                             mensaje="Planta no encontrada"), 404
    
    return render_template('reportes/detalle_planta.html', 
                         datos=datos_planta,
                         fecha_consulta=datetime.now().strftime("%d/%m/%Y %H:%M"))

@reporte_bp.route('/planta/<int:id_planta>/pdf')
def generar_pdf_planta(id_planta):
    """Genera PDF para una planta específica"""
    if 'usuario' not in session:
        return redirect(url_for('user.login'))
    
    datos_planta = PlantasController.obtener_reporte_completo_planta(id_planta)
    
    if not datos_planta:
        return jsonify({'error': 'Planta no encontrada'}), 404
    
    # Crear el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.5*inch,
        rightMargin=0.5*inch,
        title=f"Reporte de {datos_planta['informacion_basica']['nombreCientifico']}",
        author="Sistema de Plantas Medicinales"
    )
    
    # Estilos para el PDF
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=30,
        alignment=1,  # Centrado
        textColor=colors.darkgreen,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        alignment=1,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        spaceBefore=12,
        textColor=colors.darkgreen,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    bold_style = ParagraphStyle(
        'CustomBold',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    # Contenido del PDF
    story = []
    
    # === ENCABEZADO ===
    story.append(Paragraph("REPORTE DE PLANTA MEDICINAL", title_style))
    story.append(Paragraph(f"<i>{datos_planta['informacion_basica']['nombreCientifico']}</i>", subtitle_style))
    story.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y a las %H:%M')}", normal_style))
    story.append(Spacer(1, 20))
    
    # === INFORMACIÓN BÁSICA ===
    story.append(Paragraph("1. INFORMACIÓN BÁSICA", heading_style))
    
    info_basica = datos_planta['informacion_basica']
    basic_data = [
        ['<b>Nombre Científico</b>', f"<i>{info_basica['nombreCientifico']}</i>"],
        ['<b>Familia</b>', info_basica['nomFamilia'] or 'No especificada'],
        ['<b>Nombres Comunes</b>', info_basica['nombres_comunes'] or 'No registrados'],
        ['<b>ID de la Planta</b>', str(info_basica['idPlanta'])]
    ]
    
    basic_table = Table(basic_data, colWidths=[2*inch, 4*inch])
    basic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(basic_table)
    story.append(Spacer(1, 20))
    
    # === DATOS MORFOLÓGICOS ===
    if datos_planta['datos_morfologicos']:
        story.append(Paragraph("2. CARACTERÍSTICAS MORFOLÓGICAS", heading_style))
        
        for i, dato in enumerate(datos_planta['datos_morfologicos'], 1):
            story.append(Paragraph(f"<b>Descripción {i}:</b>", bold_style))
            # Dividir texto largo en párrafos más manejables
            texto_morfologico = dato['datoMorfologico']
            if len(texto_morfologico) > 500:
                # Dividir en párrafos de máximo 500 caracteres
                palabras = texto_morfologico.split(' ')
                parrafo_actual = []
                longitud_actual = 0
                
                for palabra in palabras:
                    if longitud_actual + len(palabra) + 1 <= 500:
                        parrafo_actual.append(palabra)
                        longitud_actual += len(palabra) + 1
                    else:
                        if parrafo_actual:
                            story.append(Paragraph(' '.join(parrafo_actual), normal_style))
                        parrafo_actual = [palabra]
                        longitud_actual = len(palabra)
                
                if parrafo_actual:
                    story.append(Paragraph(' '.join(parrafo_actual), normal_style))
            else:
                story.append(Paragraph(texto_morfologico, normal_style))
            
            story.append(Spacer(1, 8))
        
        story.append(Spacer(1, 15))
    
    # === UBICACIONES GEOGRÁFICAS ===
    if datos_planta['ubicaciones']:
        story.append(Paragraph("3. DISTRIBUCIÓN GEOGRÁFICA", heading_style))
        
        ubicaciones_data = [['<b>Región</b>', '<b>Provincia</b>', '<b>Ecoregión</b>']]
        
        for ubicacion in datos_planta['ubicaciones']:
            ubicaciones_data.append([
                ubicacion['region'] or 'No especificada',
                ubicacion['nombreProvincia'] or 'No especificada',
                ubicacion['ecoregion'] or 'No especificada'
            ])
        
        ubicaciones_table = Table(ubicaciones_data, colWidths=[2*inch, 2*inch, 2*inch])
        ubicaciones_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(ubicaciones_table)
        story.append(Spacer(1, 20))
    
    # === USOS MEDICINALES ===
    if datos_planta['usos_medicinales']:
        story.append(Paragraph("4. USOS MEDICINALES", heading_style))
        
        for i, uso in enumerate(datos_planta['usos_medicinales'], 1):
            story.append(Paragraph(f"<b>Uso {i}:</b>", subheading_style))
            
            uso_data = [
                ['<b>Parte utilizada</b>', uso['parte'] or 'No especificada'],
                ['<b>Uso medicinal</b>', uso['uso'] or 'No especificado'],
                ['<b>Preparación</b>', uso['preparacion'] or 'No especificada'],
                ['<b>Contraindicaciones</b>', uso['contraIndicaciones'] or 'No especificadas']
            ]
            
            uso_table = Table(uso_data, colWidths=[1.5*inch, 4.5*inch])
            uso_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(uso_table)
            story.append(Spacer(1, 12))
        
        story.append(Spacer(1, 15))
    
    # === SABERES CULTURALES ===
    if datos_planta['saberes_culturales']:
        story.append(Paragraph("5. SABERES CULTURALES", heading_style))
        
        for i, saber in enumerate(datos_planta['saberes_culturales'], 1):
            story.append(Paragraph(f"<b>Conocimiento tradicional {i}:</b>", subheading_style))
            story.append(Paragraph(saber['descripcionSaber'], normal_style))
            story.append(Spacer(1, 10))
        
        story.append(Spacer(1, 15))
    
    # === APORTES DE EXPERTOS ===
    if datos_planta['aportes_expertos']:
        story.append(Paragraph("6. APORTES DE EXPERTOS", heading_style))
        
        for i, aporte in enumerate(datos_planta['aportes_expertos'], 1):
            story.append(Paragraph(f"<b>Aporte {i}:</b>", subheading_style))
            
            aporte_data = [
                ['<b>Experto</b>', aporte['nombre_experto']],
                ['<b>Tipo de aporte</b>', aporte['tipo_aporte']],
                ['<b>Fecha</b>', aporte['fecha'].strftime('%d/%m/%Y') if aporte['fecha'] else 'No especificada'],
                ['<b>Descripción</b>', aporte['descripcion'] or 'No especificada'],
                ['<b>Contacto</b>', f"DNI: {aporte['DNI']}, Tel: {aporte['telefono'] or 'No especificado'}"]
            ]
            
            aporte_table = Table(aporte_data, colWidths=[1.5*inch, 4.5*inch])
            aporte_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightyellow),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(aporte_table)
            story.append(Spacer(1, 12))
        
        story.append(Spacer(1, 15))
    
    # === INFORMACIÓN DE REGISTRO ===
    if datos_planta['empleados_registro']:
        story.append(Paragraph("7. INFORMACIÓN DE REGISTRO", heading_style))
        
        registro_data = [['<b>Empleado</b>', '<b>DNI</b>', '<b>Correo</b>', '<b>Cargo</b>']]
        
        for empleado in datos_planta['empleados_registro']:
            registro_data.append([
                empleado['nombre_empleado'],
                empleado['DNI'],
                empleado['correo'],
                empleado['cargo']
            ])
        
        registro_table = Table(registro_data, colWidths=[2*inch, 1*inch, 2*inch, 1*inch])
        registro_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(registro_table)
        story.append(Spacer(1, 20))
    
    # === RESUMEN ESTADÍSTICO ===
    if datos_planta['resumen']:
        story.append(Paragraph("8. RESUMEN ESTADÍSTICO", heading_style))
        
        resumen = datos_planta['resumen']
        stats_data = [
            ['<b>Concepto</b>', '<b>Cantidad</b>'],
            ['Total de imágenes', str(resumen['total_imagenes'])],
            ['Total de usos medicinales', str(resumen['total_usos'])],
            ['Total de saberes culturales', str(resumen['total_saberes'])],
            ['Total de aportes de expertos', str(resumen['total_aportes'])],
            ['Estado de la planta', resumen['estado_planta']]
        ]
        
        stats_table = Table(stats_data, colWidths=[3*inch, 1.5*inch])
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 20))
    
    # === PIE DE PÁGINA ===
    story.append(Spacer(1, 30))
    story.append(Paragraph("_" * 80, normal_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        f"Reporte generado por el Sistema de Plantas Medicinales - {datetime.now().strftime('%d de %B de %Y')}",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, alignment=1, textColor=colors.grey)
    ))
    
    # Construir el PDF
    try:
        doc.build(story)
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        response = make_response(pdf_data)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename="Planta_{datos_planta["informacion_basica"]["nombreCientifico"].replace(" ", "_")}_{datetime.now().strftime("%Y%m%d")}.pdf"'
        
        return response
        
    except Exception as e:
        logger.error(f"Error al generar PDF: {e}")
        buffer.close()
        return jsonify({'error': 'Error al generar el PDF'}), 500

@reporte_bp.route('/estadisticas')
def mostrar_estadisticas():
    """Muestra estadísticas generales del sistema"""
    if 'usuario' not in session:
        return redirect(url_for('user.login'))
    
    estadisticas = PlantasController.obtener_estadisticas_generales()
    
    return render_template('reportes/estadisticas.html', 
                         estadisticas=estadisticas,
                         fecha_generacion=datetime.now().strftime("%d/%m/%Y %H:%M"))

@reporte_bp.route('/api/planta/<int:id_planta>')
def api_datos_planta(id_planta):
    """API endpoint para obtener datos de una planta en formato JSON"""
    if 'usuario' not in session:
        return jsonify({'error': 'No autorizado'}), 401
    
    datos_planta = PlantasController.obtener_reporte_completo_planta(id_planta)
    
    if not datos_planta:
        return jsonify({'error': 'Planta no encontrada'}), 404
    
    return jsonify(datos_planta)

# Función auxiliar para verificar sesión
def verificar_sesion():
    """Verifica si el usuario tiene sesión activa"""
    return 'usuario' in session