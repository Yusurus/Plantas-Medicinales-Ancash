from flask import Blueprint, render_template, jsonify, request
from config.db import get_connection
import mysql.connector

reportes_bp2 = Blueprint("reportes_bp2", __name__)


@reportes_bp2.route("/reportes_grafico")
def mostrar_reportes():
    """Renderizar la página principal de reportes"""
    try:
        # Obtener datos para los reportes
        reportes_data = obtener_datos_reportes()
        return render_template("reportes/reporte_grafico.html", reportes=reportes_data)
    except Exception as e:
        print(f"Error al mostrar reportes: {e}")
        return render_template(
            "reportes/reporte2.html", reportes=None, error="Error al cargar los datos"
        )


@reportes_bp2.route("/api/reportes/plantas-por-familia")
def plantas_por_familia():
    """API endpoint para obtener plantas agrupadas por familia"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT 
            fp.nomFamilia as familia,
            COUNT(p.idPlanta) as cantidad_plantas
        FROM familias_plantas fp
        LEFT JOIN plantas p ON fp.idfamiliaPlanta = p.fk_familiasplantas
		WHERE 
        p.idPlanta IN (SELECT DISTINCT
                archivacionesplantas.fk_plantas
            FROM
                archivacionesplantas)
            IS FALSE
        GROUP BY fp.idfamiliaPlanta, fp.nomFamilia
        ORDER BY cantidad_plantas DESC
        """

        cursor.execute(query)
        resultado = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(resultado)

    except mysql.connector.Error as e:
        print(f"Error de base de datos: {e}")
        return jsonify({"error": "Error al obtener datos"}), 500


@reportes_bp2.route("/api/reportes/plantas-por-region")
def plantas_por_region():
    """API endpoint para obtener plantas por región"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT 
            r.region,
            COUNT(DISTINCT p.idPlanta) as cantidad_plantas
        FROM regiones r
        LEFT JOIN ubicaciones_nombres un ON r.idRegion = un.fk_regiones
        LEFT JOIN nombres_comunes nc ON un.fk_nombres_comunes = nc.idNombrecomun
        LEFT JOIN plantas p ON nc.fk_plantas = p.idPlanta
        WHERE
        p.idPlanta IN (SELECT DISTINCT
                archivacionesplantas.fk_plantas
            FROM
                archivacionesplantas)
            IS FALSE
        GROUP BY r.idRegion, r.region
        ORDER BY cantidad_plantas DESC
        """

        cursor.execute(query)
        resultado = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(resultado)

    except mysql.connector.Error as e:
        print(f"Error de base de datos: {e}")
        return jsonify({"error": "Error al obtener datos"}), 500


@reportes_bp2.route("/api/reportes/resumen-general")
def resumen_general():
    """API endpoint para obtener resumen general de la base de datos"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Total de plantas
        cursor.execute("SELECT COUNT(*) as total FROM plantas")
        total_plantas = cursor.fetchone()["total"]

        # Total de familias
        cursor.execute("SELECT COUNT(*) as total FROM familias_plantas")
        total_familias = cursor.fetchone()["total"]

        # Total de saberes culturales
        cursor.execute("SELECT COUNT(*) as total FROM saberes_culturales")
        total_saberes = cursor.fetchone()["total"]

        # Total de usos registrados
        cursor.execute("SELECT COUNT(*) as total FROM usos")
        total_usos = cursor.fetchone()["total"]

        # Total de regiones
        cursor.execute("SELECT COUNT(*) as total FROM regiones")
        total_regiones = cursor.fetchone()["total"]

        cursor.close()
        connection.close()

        resumen = {
            "total_plantas": total_plantas,
            "total_familias": total_familias,
            "total_saberes": total_saberes,
            "total_usos": total_usos,
            "total_regiones": total_regiones,
        }

        return jsonify(resumen)

    except mysql.connector.Error as e:
        print(f"Error de base de datos: {e}")
        return jsonify({"error": "Error al obtener datos"}), 500


@reportes_bp2.route("/api/reportes/plantas-detalles", methods=["GET"])
def plantas_detalles():
    """
    API endpoint para obtener una lista de plantas basada en un filtro (familia o región),
    """
    tipo = request.args.get("tipo")
    valor = request.args.get("valor")

    if not tipo or not valor:
        return jsonify({"error": "Parámetros 'tipo' y 'valor' son requeridos."}), 400

    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query = ""
        params = {}

        if tipo == "familia":
            query = """
            SELECT 
                v.idPlanta, 
                v.nombreCientifico, 
                v.linkImagen, 
                v.nombres_comunes,
                v.nomFamilia
            FROM vta_plantas_activas v
            WHERE v.nomFamilia = %s
            ORDER BY v.nombreCientifico;
            """
            params = (valor,)
        elif tipo == "region":
            query = """
            SELECT 
                p.idPlanta, 
                p.nombreCientifico, 
                (SELECT li.linkImagen FROM linksimagenes li WHERE li.fk_plantas = p.idPlanta LIMIT 1) AS linkImagen,
                GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') AS nombres_comunes,
                r.region
            FROM plantas p
            LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
            LEFT JOIN ubicaciones_nombres un ON nc.idNombrecomun = un.fk_nombres_comunes
            LEFT JOIN regiones r ON un.fk_regiones = r.idRegion
            WHERE r.region = %s
                AND p.idPlanta IN (SELECT DISTINCT fk_plantas FROM archivacionesplantas) IS FALSE
            GROUP BY p.idPlanta, p.nombreCientifico, r.region
            ORDER BY p.nombreCientifico;
            """
            params = (valor,)
        else:
            return jsonify(
                {"error": "Tipo de filtro inválido. Use 'familia' o 'region'."}
            ), 400

        cursor.execute(query, params)
        plantas = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(plantas)

    except mysql.connector.Error as e:
        print(f"Error de base de datos al obtener detalles de plantas: {e}")
        return jsonify({"error": "Error al obtener detalles de plantas"}), 500


def obtener_datos_reportes():
    """Función auxiliar para obtener todos los datos necesarios para los reportes"""
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Plantas más registradas (con más información)
        query_plantas_completas = """
        SELECT 
            p.nombreCientifico,
            fp.nomFamilia,
            COUNT(DISTINCT nc.idNombrecomun) as nombres_comunes,
            COUNT(DISTINCT sc.idSaberes) as saberes_culturales,
            COUNT(DISTINCT u.idUsos) as usos_registrados,
            COUNT(DISTINCT dm.idDatomorfologico) as datos_morfologicos
        FROM plantas p
        LEFT JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        LEFT JOIN nombres_comunes nc ON p.idPlanta = nc.fk_plantas
        LEFT JOIN saberes_culturales sc ON p.idPlanta = sc.fk_plantas
        LEFT JOIN usos u ON p.idPlanta = u.fk_plantas
        LEFT JOIN datos_morfologicos dm ON p.idPlanta = dm.fk_plantas
        GROUP BY p.idPlanta, p.nombreCientifico, fp.nomFamilia
        ORDER BY (nombres_comunes + saberes_culturales + usos_registrados + datos_morfologicos) DESC
        LIMIT 10
        """

        cursor.execute(query_plantas_completas)
        plantas_completas = cursor.fetchall()

        cursor.close()
        connection.close()

        return {"plantas_completas": plantas_completas}

    except mysql.connector.Error as e:
        print(f"Error al obtener datos de reportes: {e}")
        return None
