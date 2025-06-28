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
        # Query principal que obtiene toda la información de las plantas
        query = """
        SELECT 
            p.idPlanta,
            p.nombreCientifico,
            fp.nomFamilia,
            GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') as nombres_comunes,
            GROUP_CONCAT(DISTINCT r.region SEPARATOR ', ') as regiones,
            GROUP_CONCAT(DISTINCT er.ecoregion SEPARATOR ', ') as ecoregiones,
            dm.datoMorfologico,
            GROUP_CONCAT(DISTINCT CONCAT(u.parte, ' - ', u.uso, ' (Prep: ', u.preparacion, ')') SEPARATOR '; ') as usos,
            GROUP_CONCAT(DISTINCT sc.descripcionSaber SEPARATOR '; ') as saberes_culturales,
            GROUP_CONCAT(DISTINCT li.linkImagen SEPARATOR '; ') as imagenes
        FROM plantas p
        LEFT JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        LEFT JOIN ubicaciones_nombres un ON nc.idNombrecomun = un.fk_nombres_comunes
        LEFT JOIN regiones r ON un.fk_regiones = r.idRegion
        LEFT JOIN ecoregiones er ON p.idPlanta = er.fk_plantas
        LEFT JOIN region_ecoregion re ON er.idecoregion = re.fk_ecoregiones
        LEFT JOIN datos_morfologicos dm ON p.idPlanta = dm.fk_plantas
        LEFT JOIN usos u ON p.idPlanta = u.fk_plantas
        LEFT JOIN saberes_culturales sc ON p.idPlanta = sc.fk_plantas
        LEFT JOIN linksimagenes li ON p.idPlanta = li.fk_plantas
        GROUP BY p.idPlanta, p.nombreCientifico, fp.nomFamilia, dm.datoMorfologico
        ORDER BY p.nombreCientifico
        """
        
        cursor.execute(query)
        plantas = cursor.fetchall()
        
        # Obtener estadísticas adicionales
        stats_query = """
        SELECT 
            (SELECT COUNT(*) FROM plantas) as total_plantas,
            (SELECT COUNT(*) FROM familias_plantas) as total_familias,
            (SELECT COUNT(*) FROM nombres_comunes) as total_nombres_comunes,
            (SELECT COUNT(*) FROM usos) as total_usos,
            (SELECT COUNT(*) FROM saberes_culturales) as total_saberes,
            (SELECT COUNT(*) FROM regiones) as total_regiones
        """
        
        cursor.execute(stats_query)
        estadisticas = cursor.fetchone()
        
        return plantas, estadisticas
        
    except mysql.connector.Error as e:
        print(f"Error al obtener datos: {e}")
        return [], {}
    finally:
        cursor.close()
        connection.close()

@reporte_bp.route('/plantas_pdf')
def reporte_plantas():
    """Muestra el reporte de plantas en HTML"""
    if 'usuario' not in session:
        return redirect(url_for('user.login'))
    
    plantas, estadisticas = obtener_datos_completos_plantas()
    
    return render_template('reportes/reporte_pdf.html', 
                         plantas=plantas, 
                         estadisticas=estadisticas,
                         fecha_generacion=datetime.now().strftime("%d/%m/%Y %H:%M"))

@reporte_bp.route('/reporte_plantas_pdf')
def generar_pdf():
    """Genera y muestra el reporte en formato PDF (vista previa en navegador)"""
    if 'usuario' not in session:
        return redirect(url_for('user.login'))
    
    plantas, estadisticas = obtener_datos_completos_plantas()
    
    # Crear el PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        topMargin=0.5*inch,
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
        ['Total de Plantas', str(estadisticas.get('total_plantas', 0))],
        ['Total de Familias', str(estadisticas.get('total_familias', 0))],
        ['Total de Nombres Comunes', str(estadisticas.get('total_nombres_comunes', 0))],
        ['Total de Usos Registrados', str(estadisticas.get('total_usos', 0))],
        ['Total de Saberes Culturales', str(estadisticas.get('total_saberes', 0))],
        ['Total de Regiones', str(estadisticas.get('total_regiones', 0))]
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 1.5*inch])
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
    story.append(PageBreak())
    
    # Detalles de cada planta
    story.append(Paragraph("DETALLE DE PLANTAS", heading_style))
    
    for i, planta in enumerate(plantas):
        if i > 0:
            story.append(Spacer(1, 15))
        
        # Información básica de la planta
        plant_data = [
            ['Nombre Científico', planta.get('nombreCientifico', 'N/A')],
            ['Familia', planta.get('nomFamilia', 'N/A')],
            ['Nombres Comunes', planta.get('nombres_comunes', 'N/A') or 'N/A'],
            ['Regiones', planta.get('regiones', 'N/A') or 'N/A'],
            ['Ecoregiones', planta.get('ecoregiones', 'N/A') or 'N/A']
        ]
        
        plant_table = Table(plant_data, colWidths=[2*inch, 4*inch])
        plant_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        story.append(plant_table)
        story.append(Spacer(1, 10))
        
        # Datos morfológicos
        if planta.get('datoMorfologico'):
            story.append(Paragraph("<b>Datos Morfológicos:</b>", normal_style))
            morfologia_text = planta['datoMorfologico'][:500] + "..." if len(planta['datoMorfologico']) > 500 else planta['datoMorfologico']
            story.append(Paragraph(morfologia_text, normal_style))
            story.append(Spacer(1, 8))
        
        # Usos
        if planta.get('usos'):
            story.append(Paragraph("<b>Usos:</b>", normal_style))
            usos_text = planta['usos'][:400] + "..." if len(planta['usos']) > 400 else planta['usos']
            story.append(Paragraph(usos_text, normal_style))
            story.append(Spacer(1, 8))
        
        # Saberes culturales
        if planta.get('saberes_culturales'):
            story.append(Paragraph("<b>Saberes Culturales:</b>", normal_style))
            saberes_text = planta['saberes_culturales'][:400] + "..." if len(planta['saberes_culturales']) > 400 else planta['saberes_culturales']
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