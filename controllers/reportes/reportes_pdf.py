from flask import Blueprint, render_template, session, redirect, url_for, make_response
from config.db import get_connection
import mysql.connector
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime

reporte_bp = Blueprint('reporte', __name__)

def obtener_datos_completos_plantas():
    """Obtiene todos los datos relacionados con las plantas de la base de datos"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:

        query = """SELECT * FROM vta_reportesPlantasGeneral"""
        # query = """
        # SELECT 
        #     p.idPlanta,
        #     p.nombreCientifico,
        #     fp.nomFamilia,
        #     GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') as nombres_comunes,
        #     GROUP_CONCAT(DISTINCT r.region SEPARATOR ', ') as regiones,
        #     GROUP_CONCAT(DISTINCT pr.nombreProvincia SEPARATOR ', ') as provincias,
        #     GROUP_CONCAT(DISTINCT eco.ecoregion SEPARATOR ', ') as ecoregiones,
        #     GROUP_CONCAT(DISTINCT dm.datoMorfologico SEPARATOR '; ') as datos_morfologicos,
        #     GROUP_CONCAT(DISTINCT CONCAT(
        #         'Parte: ', u.parte, 
        #         ' | Uso: ', u.uso, 
        #         ' | Preparación: ', u.preparacion,
        #         CASE WHEN u.contraIndicaciones != '' THEN CONCAT(' | Contraindicaciones: ', u.contraIndicaciones) ELSE '' END
        #     ) SEPARATOR '; ') as usos,
        #     GROUP_CONCAT(DISTINCT sc.descripcionSaber SEPARATOR '; ') as saberes_culturales,
        #     GROUP_CONCAT(DISTINCT li.linkImagen SEPARATOR '; ') as imagenes
        # FROM plantas p
        # INNER JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        # LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        # LEFT JOIN ubicaciones_nombres un ON nc.idNombrecomun = un.fk_nombres_comunes
        # LEFT JOIN regiones r ON un.fk_regiones = r.idRegion
        # LEFT JOIN ecoregion_planta ep ON p.idPlanta = ep.fk_plantas
        # LEFT JOIN ecoregiones eco ON ep.fk_ecoregiones = eco.idecoregion
        # LEFT JOIN provincia_ecoregion pe ON eco.idecoregion = pe.fk_ecoregiones
        # LEFT JOIN provincias pr ON pe.fk_provincias = pr.idprovincias
        # LEFT JOIN datos_morfologicos dm ON p.idPlanta = dm.fk_plantas
        # LEFT JOIN usos u ON p.idPlanta = u.fk_plantas
        # LEFT JOIN saberes_culturales sc ON p.idPlanta = sc.fk_plantas
        # LEFT JOIN linksimagenes li ON p.idPlanta = li.fk_plantas
        # WHERE p.idPlanta NOT IN (
        #     SELECT DISTINCT fk_plantas FROM archivacionesplantas
        # )
        # GROUP BY p.idPlanta, p.nombreCientifico, fp.nomFamilia
        # ORDER BY p.nombreCientifico
        # """
        
        cursor.execute(query)
        plantas = cursor.fetchall()
        
        # Obtener estadísticas adicionales
        stats_query = """SELECT * FROM vta_reporteEstadisticaGeneral"""

        # stats_query = """
        # SELECT 
        #     (SELECT COUNT(*) FROM plantas WHERE idPlanta NOT IN (
        #         SELECT DISTINCT fk_plantas FROM archivacionesplantas
        #     )) as total_plantas_activas,
        #     (SELECT COUNT(*) FROM plantas) as total_plantas,
        #     (SELECT COUNT(*) FROM familias_plantas) as total_familias,
        #     (SELECT COUNT(*) FROM nombres_comunes) as total_nombres_comunes,
        #     (SELECT COUNT(*) FROM usos WHERE fk_plantas NOT IN (
        #         SELECT DISTINCT fk_plantas FROM archivacionesplantas
        #     )) as total_usos_activos,
        #     (SELECT COUNT(*) FROM saberes_culturales WHERE fk_plantas NOT IN (
        #         SELECT DISTINCT fk_plantas FROM archivacionesplantas
        #     )) as total_saberes_activos,
        #     (SELECT COUNT(*) FROM regiones) as total_regiones,
        #     (SELECT COUNT(*) FROM ecoregiones) as total_ecoregiones,
        #     (SELECT COUNT(*) FROM provincias) as total_provincias,
        #     (SELECT COUNT(*) FROM archivacionesplantas) as total_plantas_archivadas
        # """
        
        cursor.execute(stats_query)
        estadisticas = cursor.fetchone()
        
        return plantas, estadisticas
        
    except mysql.connector.Error as e:
        print(f"Error al obtener datos: {e}")
        return [], {}
    finally:
        cursor.close()
        connection.close()

def obtener_plantas_por_familia():
    """Obtiene el conteo de plantas por familia"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = """SELECT * FROM vta_reporteolantasPorFamilia"""
        # query = """
        # SELECT 
        #     fp.nomFamilia,
        #     COUNT(p.idPlanta) as cantidad_plantas
        # FROM familias_plantas fp
        # LEFT JOIN plantas p ON fp.idfamiliaPlanta = p.fk_familiasplantas
        # WHERE p.idPlanta IS NULL OR p.idPlanta NOT IN (
        #     SELECT DISTINCT fk_plantas FROM archivacionesplantas
        # )
        # GROUP BY fp.idfamiliaPlanta, fp.nomFamilia
        # HAVING COUNT(p.idPlanta) > 0
        # ORDER BY cantidad_plantas DESC, fp.nomFamilia
        # """
        
        cursor.execute(query)
        return cursor.fetchall()
        
    except mysql.connector.Error as e:
        print(f"Error al obtener datos por familia: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def obtener_plantas_por_ecoregion():
    """Obtiene el conteo de plantas por ecoregión"""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = """SELECT * FROM vta_reporteolantasPorEcorregion"""
        # query = """
        # SELECT 
        #     eco.ecoregion,
        #     COUNT(DISTINCT p.idPlanta) as cantidad_plantas
        # FROM ecoregiones eco
        # LEFT JOIN ecoregion_planta ep ON eco.idecoregion = ep.fk_ecoregiones
        # LEFT JOIN plantas p ON ep.fk_plantas = p.idPlanta
        # WHERE p.idPlanta IS NULL OR p.idPlanta NOT IN (
        #     SELECT DISTINCT fk_plantas FROM archivacionesplantas
        # )
        # GROUP BY eco.idecoregion, eco.ecoregion
        # HAVING COUNT(DISTINCT p.idPlanta) > 0
        # ORDER BY cantidad_plantas DESC, eco.ecoregion
        # """
        
        cursor.execute(query)
        return cursor.fetchall()
        
    except mysql.connector.Error as e:
        print(f"Error al obtener datos por ecoregión: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

@reporte_bp.route('/plantas_pdf')
def reporte_plantas():
    """Muestra el reporte de plantas en HTML"""
    if 'usuario' not in session:
        return redirect(url_for('user.login'))
    
    plantas, estadisticas = obtener_datos_completos_plantas()
    plantas_por_familia = obtener_plantas_por_familia()
    plantas_por_ecoregion = obtener_plantas_por_ecoregion()
    
    return render_template('reportes/reporte_pdf.html', 
                         plantas=plantas, 
                         estadisticas=estadisticas,
                         plantas_por_familia=plantas_por_familia,
                         plantas_por_ecoregion=plantas_por_ecoregion,
                         fecha_generacion=datetime.now().strftime("%d/%m/%Y %H:%M"))

@reporte_bp.route('/reporte_plantas_pdf')
def generar_pdf():
    """Genera y muestra el reporte en formato PDF (vista previa en navegador)"""
    if 'usuario' not in session:
        return redirect(url_for('user.login'))
    
    plantas, estadisticas = obtener_datos_completos_plantas()
    plantas_por_familia = obtener_plantas_por_familia()
    plantas_por_ecoregion = obtener_plantas_por_ecoregion()
    
    # Crear el PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch,
        title="Reporte de Plantas Medicinales",
        author="Sistema de Plantas Medicinales",
        subject="Reporte completo de plantas medicinales registradas"
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Centrado
        textColor=colors.darkgreen
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=8,
        textColor=colors.darkred
    )
    
    normal_style = styles['Normal']
    normal_style.fontSize = 9
    
    # Contenido del PDF
    story = []
    
    # Título
    story.append(Paragraph("REPORTE COMPLETO DE PLANTAS MEDICINALES", title_style))
    story.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')}", normal_style))
    story.append(Spacer(1, 20))
    
    # Estadísticas generales
    story.append(Paragraph("ESTADÍSTICAS GENERALES", heading_style))
    stats_data = [
        ['Concepto', 'Cantidad'],
        ['Total de Plantas Activas', str(estadisticas.get('total_plantas_activas', 0))],
        ['Total de Plantas (incluyendo archivadas)', str(estadisticas.get('total_plantas', 0))],
        ['Plantas Archivadas', str(estadisticas.get('total_plantas_archivadas', 0))],
        ['Total de Familias', str(estadisticas.get('total_familias', 0))],
        ['Total de Nombres Comunes', str(estadisticas.get('total_nombres_comunes', 0))],
        ['Total de Usos Activos', str(estadisticas.get('total_usos_activos', 0))],
        ['Total de Saberes Culturales Activos', str(estadisticas.get('total_saberes_activos', 0))],
        ['Total de Regiones', str(estadisticas.get('total_regiones', 0))],
        ['Total de Provincias', str(estadisticas.get('total_provincias', 0))],
        ['Total de Ecoregiones', str(estadisticas.get('total_ecoregiones', 0))]
    ]
    
    stats_table = Table(stats_data, colWidths=[3.5*inch, 1.5*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(stats_table)
    story.append(Spacer(1, 20))
    
    # Distribución por familias
    if plantas_por_familia:
        story.append(Paragraph("DISTRIBUCIÓN POR FAMILIAS", heading_style))
        familia_data = [['Familia', 'Cantidad de Plantas']]
        for familia in plantas_por_familia[:10]:  # Top 10 familias
            familia_data.append([familia['nomFamilia'], str(familia['cantidad_plantas'])])
        
        familia_table = Table(familia_data, colWidths=[3.5*inch, 1.5*inch])
        familia_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(familia_table)
        story.append(Spacer(1, 20))
    
    # Distribución por ecoregiones
    if plantas_por_ecoregion:
        story.append(Paragraph("DISTRIBUCIÓN POR ECOREGIONES", heading_style))
        eco_data = [['Ecoregión', 'Cantidad de Plantas']]
        for eco in plantas_por_ecoregion:
            eco_data.append([eco['ecoregion'], str(eco['cantidad_plantas'])])
        
        eco_table = Table(eco_data, colWidths=[3.5*inch, 1.5*inch])
        eco_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkorange),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightyellow),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(eco_table)
    
    story.append(PageBreak())
    
    # Detalles de cada planta
    story.append(Paragraph("DETALLE DE PLANTAS MEDICINALES", heading_style))
    story.append(Spacer(1, 10))
    
    for i, planta in enumerate(plantas):
        if i > 0:
            story.append(Spacer(1, 15))
        
        # Título de la planta
        plant_title = f"{i+1}. {planta.get('nombreCientifico', 'N/A')}"
        story.append(Paragraph(plant_title, subheading_style))
        
        # Información básica de la planta
        plant_data = [
            ['Campo', 'Información'],
            ['Familia', planta.get('nomFamilia', 'N/A')],
            ['Nombres Comunes', planta.get('nombres_comunes', 'Sin nombres comunes registrados') or 'Sin nombres comunes registrados'],
            ['Regiones', planta.get('regiones', 'Sin regiones registradas') or 'Sin regiones registradas'],
            ['Provincias', planta.get('provincias', 'Sin provincias registradas') or 'Sin provincias registradas'],
            ['Ecoregiones', planta.get('ecoregiones', 'Sin ecoregiones registradas') or 'Sin ecoregiones registradas']
        ]
        
        plant_table = Table(plant_data, colWidths=[1.5*inch, 4.5*inch])
        plant_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        story.append(plant_table)
        story.append(Spacer(1, 10))
        
        # Datos morfológicos
        if planta.get('datos_morfologicos'):
            story.append(Paragraph("<b>Datos Morfológicos:</b>", normal_style))
            morfologia_text = planta['datos_morfologicos']
            if len(morfologia_text) > 600:
                morfologia_text = morfologia_text[:600] + "..."
            story.append(Paragraph(morfologia_text, normal_style))
            story.append(Spacer(1, 8))
        
        # Usos
        if planta.get('usos'):
            story.append(Paragraph("<b>Usos Medicinales:</b>", normal_style))
            usos_text = planta['usos']
            if len(usos_text) > 600:
                usos_text = usos_text[:600] + "..."
            story.append(Paragraph(usos_text, normal_style))
            story.append(Spacer(1, 8))
        
        # Saberes culturales
        if planta.get('saberes_culturales'):
            story.append(Paragraph("<b>Saberes Culturales:</b>", normal_style))
            saberes_text = planta['saberes_culturales']
            if len(saberes_text) > 600:
                saberes_text = saberes_text[:600] + "..."
            story.append(Paragraph(saberes_text, normal_style))
            story.append(Spacer(1, 8))
        
        # Separador entre plantas
        if i < len(plantas) - 1:
            story.append(Paragraph("_" * 80, normal_style))
    
    # Construir el PDF
    doc.build(story)
    
    # Preparar la respuesta para mostrar en el navegador
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    buffer.close()
    
    # Configurar headers para vista previa en navegador
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'inline; filename="Reporte_Plantas_Medicinales_{datetime.now().strftime("%Y%m%d_%H%M")}.pdf"'
    
    return response
