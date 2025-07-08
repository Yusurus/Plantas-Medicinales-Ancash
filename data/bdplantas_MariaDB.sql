-- --------------------------------------------------------
-- Host:                         bdplantas.cpikeig8qwsl.us-east-1.rds.amazonaws.com
-- Versión del servidor:         11.4.4-MariaDB-log - managed by https://aws.amazon.com/rds/
-- SO del servidor:              Linux
-- HeidiSQL Versión:             12.10.0.7000
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para bdplantas
CREATE DATABASE IF NOT EXISTS `bdplantas` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;
USE `bdplantas`;

-- Volcando estructura para tabla bdplantas.aportes_expertos
CREATE TABLE IF NOT EXISTS `aportes_expertos` (
  `idAporteExperto` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `descripcion` text NOT NULL,
  `fk_personas` int(11) NOT NULL,
  `fk_plantas` int(11) NOT NULL,
  `fk_tipos_aportes` int(11) NOT NULL,
  PRIMARY KEY (`idAporteExperto`),
  KEY `fk_persona` (`fk_personas`),
  KEY `fk_planta` (`fk_plantas`),
  KEY `fk_tipoAporte` (`fk_tipos_aportes`),
  CONSTRAINT `aporte_experto_ibfk_1` FOREIGN KEY (`fk_personas`) REFERENCES `personas` (`idPersona`),
  CONSTRAINT `aporte_experto_ibfk_2` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`),
  CONSTRAINT `aporte_experto_ibfk_3` FOREIGN KEY (`fk_tipos_aportes`) REFERENCES `tipos_aportes` (`idTipoAporte`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.archivacionesplantas
CREATE TABLE IF NOT EXISTS `archivacionesplantas` (
  `idArchivaPlanta` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `motivo` text NOT NULL,
  `fk_plantas` int(11) NOT NULL,
  `fk_empleados` int(11) NOT NULL,
  PRIMARY KEY (`idArchivaPlanta`),
  KEY `fk_plantas` (`fk_plantas`),
  KEY `empleado_idEmpleado` (`fk_empleados`),
  CONSTRAINT `archivacionesplanta_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`),
  CONSTRAINT `archivacionesplanta_ibfk_2` FOREIGN KEY (`fk_empleados`) REFERENCES `empleados` (`idEmpleado`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.archivaciones_saberes
CREATE TABLE IF NOT EXISTS `archivaciones_saberes` (
  `idArchivaSaber` int(11) NOT NULL AUTO_INCREMENT,
  `fechaArchivaSaber` date NOT NULL,
  `motivoArchivaSaber` text NOT NULL,
  `fk_saberes_culturales` int(11) NOT NULL,
  `fk_empleados` int(11) NOT NULL,
  PRIMARY KEY (`idArchivaSaber`),
  KEY `fk_saberes` (`fk_saberes_culturales`),
  KEY `empleado_idEmpleado` (`fk_empleados`),
  CONSTRAINT `archivacionessaberes_ibfk_1` FOREIGN KEY (`fk_saberes_culturales`) REFERENCES `saberes_culturales` (`idSaberes`),
  CONSTRAINT `archivacionessaberes_ibfk_2` FOREIGN KEY (`fk_empleados`) REFERENCES `empleados` (`idEmpleado`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.archivaciones_ubicaciones
CREATE TABLE IF NOT EXISTS `archivaciones_ubicaciones` (
  `idArchivaUbi` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `motivo` text NOT NULL,
  `fk_idempleados` int(11) NOT NULL,
  `fk_ecoregion_plantas` int(11) NOT NULL,
  PRIMARY KEY (`idArchivaUbi`),
  KEY `empleado_idEmpleado` (`fk_idempleados`),
  KEY `ecoregiones_idecoregion` (`fk_ecoregion_plantas`),
  CONSTRAINT `archivacionesubicaciones_ibfk_2` FOREIGN KEY (`fk_idempleados`) REFERENCES `empleados` (`idEmpleado`),
  CONSTRAINT `archivacionesubicaciones_ibfk_3` FOREIGN KEY (`fk_ecoregion_plantas`) REFERENCES `ecoregion_planta` (`idecoregion_planta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.archivaciones_usos
CREATE TABLE IF NOT EXISTS `archivaciones_usos` (
  `idArchivaUso` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `motivo` text NOT NULL,
  `fk_usos` int(11) NOT NULL,
  `fk_empleados` int(11) NOT NULL,
  PRIMARY KEY (`idArchivaUso`),
  KEY `fk_archivaciones_usos_usos1_idx` (`fk_usos`),
  KEY `fk_archivaciones_usos_empleados1_idx` (`fk_empleados`),
  CONSTRAINT `fk_archivaciones_usos_empleados1` FOREIGN KEY (`fk_empleados`) REFERENCES `empleados` (`idEmpleado`),
  CONSTRAINT `fk_archivaciones_usos_usos1` FOREIGN KEY (`fk_usos`) REFERENCES `usos` (`idUsos`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.cargos
CREATE TABLE IF NOT EXISTS `cargos` (
  `idCargo` int(11) NOT NULL AUTO_INCREMENT,
  `categoria` varchar(50) NOT NULL,
  `salario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idCargo`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para procedimiento bdplantas.crud_ecoregion_planta
DELIMITER //
CREATE PROCEDURE `crud_ecoregion_planta`(
    IN ev INT,
    IN i_idEcoregionPlanta INT,
    IN i_idPlanta INT,
    IN i_idEcoregion INT
)
BEGIN
    DECLARE msg_error TEXT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        GET DIAGNOSTICS CONDITION 1 msg_error = MESSAGE_TEXT;
        SELECT CONCAT('Error: ', msg_error) AS respuesta;
    END;
    START TRANSACTION;
    CASE ev
        WHEN 1 THEN -- Asociar planta con ecoregión
            IF NOT EXISTS (SELECT 1 FROM plantas WHERE idPlanta = i_idPlanta) THEN
                SELECT 'La planta especificada no existe' AS respuesta;
            ELSEIF EXISTS (SELECT 1 FROM archivacionesplantas WHERE fk_plantas = i_idPlanta) THEN
                SELECT 'La planta está archivada y no se puede asociar' AS respuesta;
            ELSEIF NOT EXISTS (SELECT 1 FROM ecoregiones WHERE idecoregion = i_idEcoregion) THEN
                SELECT 'La ecoregión especificada no existe' AS respuesta;
            ELSEIF EXISTS (
                SELECT 1 FROM ecoregion_planta 
                WHERE fk_plantas = i_idPlanta AND fk_ecoregiones = i_idEcoregion
            ) THEN
                SELECT 'La asociación ya existe' AS respuesta;
            ELSE
                INSERT INTO ecoregion_planta(fk_plantas, fk_ecoregiones)
                VALUES (i_idPlanta, i_idEcoregion);
                SELECT CONCAT('Asociación planta-ecoregión creada correctamente con ID: ', LAST_INSERT_ID()) AS respuesta;
            END IF;
        WHEN 2 THEN -- Actualizar ecoregión de la asociación
            IF NOT EXISTS (SELECT 1 FROM ecoregiones WHERE idecoregion = i_idEcoregion) THEN
                SELECT 'La ecoregión especificada no existe' AS respuesta;
            ELSE
                UPDATE ecoregion_planta
                SET fk_ecoregiones = i_idEcoregion
                WHERE idecoregion_planta = i_idEcoregionPlanta;
                IF ROW_COUNT() = 0 THEN
                    SELECT 'No se encontró la asociación especificada' AS respuesta;
                ELSE
                    SELECT 'Asociación actualizada correctamente' AS respuesta;
                END IF;
            END IF;
        WHEN 3 THEN -- elimina ecoregión de la asociación
            IF NOT EXISTS (SELECT 1 FROM ecoregion_planta WHERE idecoregion_planta = i_idEcoregionPlanta) THEN
                SELECT 'El id de planta_ecoregion especificada no existe' AS respuesta;
            ELSE
                DELETE FROM ecoregion_planta
                WHERE idecoregion_planta = i_idEcoregionPlanta;
            END IF;
        ELSE
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Evento no reconocido. Usa 1 (asociar), 2 (actualizar)';
    END CASE;
    COMMIT;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bdplantas.crud_provincias
DELIMITER //
CREATE PROCEDURE `crud_provincias`(
    IN ev INT,
    IN i_idProvincia INT,
    IN i_nombreProvincia VARCHAR(45),
    IN i_idRegion INT
)
BEGIN
    DECLARE msg_error TEXT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        GET DIAGNOSTICS CONDITION 1 msg_error = MESSAGE_TEXT;
        SELECT CONCAT('Error: ', msg_error) AS respuesta;
    END;
    START TRANSACTION;
    CASE ev
        WHEN 1 THEN -- Insertar provincia
            IF NOT EXISTS (SELECT 1 FROM regiones WHERE idRegion = i_idRegion) THEN
                SELECT 'La región especificada no existe' AS respuesta;
            ELSE
                INSERT INTO provincias(nombreProvincia, fk_regiones)
                VALUES (i_nombreProvincia, i_idRegion);
                SELECT CONCAT('Provincia "', i_nombreProvincia, '" registrada correctamente con ID: ', LAST_INSERT_ID()) AS respuesta;
            END IF;
        WHEN 2 THEN -- Actualizar provincia
            IF NOT EXISTS (SELECT 1 FROM regiones WHERE idRegion = i_idRegion) THEN
                SELECT 'La región especificada no existe' AS respuesta;
            ELSE
                UPDATE provincias
                SET nombreProvincia = i_nombreProvincia,
                    fk_regiones = i_idRegion
                WHERE idprovincias = i_idProvincia;
                IF ROW_COUNT() = 0 THEN
                    SELECT 'No se encontró la provincia especificada' AS respuesta;
                ELSE
                    SELECT 'Provincia actualizada correctamente' AS respuesta;
                END IF;
            END IF;
        WHEN 3 THEN -- Eliminar provincia
            IF EXISTS (SELECT 1 FROM provincia_ecoregion WHERE fk_provincias = i_idProvincia) THEN
                SELECT 'No se puede eliminar la provincia porque tiene ecoregiones asociadas' AS respuesta;
            ELSE
                DELETE FROM provincias WHERE idprovincias = i_idProvincia;
                IF ROW_COUNT() = 0 THEN
                    SELECT 'No se encontró la provincia especificada' AS respuesta;
                ELSE
                    SELECT 'Provincia eliminada correctamente' AS respuesta;
                END IF;
            END IF;
        ELSE
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Evento no reconocido. Usa 1 (insertar), 2 (actualizar), 3 (eliminar)';
    END CASE;
    COMMIT;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bdplantas.crud_provincia_ecoregion
DELIMITER //
CREATE PROCEDURE `crud_provincia_ecoregion`(
    IN ev INT,
    IN i_idProvincia INT,
    IN i_idEcoregion INT
)
BEGIN
    DECLARE msg_error TEXT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        GET DIAGNOSTICS CONDITION 1 msg_error = MESSAGE_TEXT;
        SELECT CONCAT('Error: ', msg_error) AS respuesta;
    END;
    START TRANSACTION;
    CASE ev
        WHEN 1 THEN -- Asociar provincia con ecoregión
            IF NOT EXISTS (SELECT 1 FROM provincias WHERE idprovincias = i_idProvincia) THEN
                SELECT 'La provincia especificada no existe' AS respuesta;
            ELSEIF NOT EXISTS (SELECT 1 FROM ecoregiones WHERE idecoregion = i_idEcoregion) THEN
                SELECT 'La ecoregión especificada no existe' AS respuesta;
            ELSEIF EXISTS (
                SELECT 1 FROM provincia_ecoregion
                WHERE fk_provincias = i_idProvincia AND fk_ecoregiones = i_idEcoregion
            ) THEN
                SELECT 'La asociación ya existe' AS respuesta;
            ELSE
                INSERT INTO provincia_ecoregion(fk_provincias, fk_ecoregiones)
                VALUES (i_idProvincia, i_idEcoregion);
                SELECT 'Asociación provincia-ecoregión creada correctamente' AS respuesta;
            END IF;
        WHEN 2 THEN -- Eliminar asociación provincia-ecoregión
            DELETE FROM provincia_ecoregion
            WHERE fk_provincias = i_idProvincia AND fk_ecoregiones = i_idEcoregion;
            IF ROW_COUNT() = 0 THEN
                SELECT 'No se encontró la asociación especificada' AS respuesta;
            ELSE
                SELECT 'Asociación eliminada correctamente' AS respuesta;
            END IF;
        ELSE
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Evento no reconocido. Usa 1 (asociar), 2 (eliminar)';
    END CASE;
    COMMIT;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bdplantas.crud_regiones
DELIMITER //
CREATE PROCEDURE `crud_regiones`(
    IN ev INT,
    IN i_idRegion INT,
    IN i_region VARCHAR(50)
)
BEGIN
    DECLARE msg_error TEXT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        GET DIAGNOSTICS CONDITION 1 msg_error = MESSAGE_TEXT;
        SELECT CONCAT('Error: ', msg_error) AS respuesta;
    END;
    START TRANSACTION;
    CASE ev
        WHEN 1 THEN -- Insertar región
            INSERT INTO regiones(region)
            VALUES (i_region);
            SELECT CONCAT('Región "', i_region, '" registrada correctamente con ID: ', LAST_INSERT_ID()) AS respuesta;
        WHEN 2 THEN -- Actualizar región
            UPDATE regiones
            SET region = i_region
            WHERE idRegion = i_idRegion;
            IF ROW_COUNT() = 0 THEN
                SELECT 'No se encontró la región especificada' AS respuesta;
            ELSE
                SELECT 'Región actualizada correctamente' AS respuesta;
            END IF;
        WHEN 3 THEN -- Eliminar región (solo si no tiene provincias asociadas)
            IF EXISTS (SELECT 1 FROM provincias WHERE fk_regiones = i_idRegion) THEN
                SELECT 'No se puede eliminar la región porque tiene provincias asociadas' AS respuesta;
            ELSE
                DELETE FROM regiones WHERE idRegion = i_idRegion;
                IF ROW_COUNT() = 0 THEN
                    SELECT 'No se encontró la región especificada' AS respuesta;
                ELSE
                    SELECT 'Región eliminada correctamente' AS respuesta;
                END IF;
            END IF;
        ELSE
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Evento no reconocido en CRUD. Usa 1 (insertar), 2 (actualizar), 3 (eliminar)';
    END CASE;
    COMMIT;
END//
DELIMITER ;

-- Volcando estructura para tabla bdplantas.datos_morfologicos
CREATE TABLE IF NOT EXISTS `datos_morfologicos` (
  `idDatomorfologico` int(11) NOT NULL AUTO_INCREMENT,
  `datoMorfologico` text NOT NULL,
  `fk_plantas` int(11) NOT NULL,
  PRIMARY KEY (`idDatomorfologico`),
  KEY `fk_plantas` (`fk_plantas`),
  CONSTRAINT `datosmorfologicos_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.ecoregiones
CREATE TABLE IF NOT EXISTS `ecoregiones` (
  `idecoregion` int(11) NOT NULL AUTO_INCREMENT,
  `ecoregion` varchar(45) NOT NULL,
  PRIMARY KEY (`idecoregion`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.ecoregion_planta
CREATE TABLE IF NOT EXISTS `ecoregion_planta` (
  `idecoregion_planta` int(11) NOT NULL AUTO_INCREMENT,
  `fk_plantas` int(11) NOT NULL,
  `fk_ecoregiones` int(11) NOT NULL,
  PRIMARY KEY (`idecoregion_planta`),
  KEY `fk_ecoregion_planta_plantas1_idx` (`fk_plantas`),
  KEY `fk_ecoregion_planta_ecoregiones1_idx` (`fk_ecoregiones`),
  CONSTRAINT `fk_ecoregion_planta_ecoregiones1` FOREIGN KEY (`fk_ecoregiones`) REFERENCES `ecoregiones` (`idecoregion`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_ecoregion_planta_plantas1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.empleados
CREATE TABLE IF NOT EXISTS `empleados` (
  `idEmpleado` int(11) NOT NULL AUTO_INCREMENT,
  `correo` varchar(50) NOT NULL,
  `fk_personas` int(11) NOT NULL,
  `fk_cargos` int(11) NOT NULL,
  PRIMARY KEY (`idEmpleado`),
  KEY `fk_personas` (`fk_personas`),
  KEY `fk_cargos` (`fk_cargos`),
  CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`fk_personas`) REFERENCES `personas` (`idPersona`),
  CONSTRAINT `empleado_ibfk_2` FOREIGN KEY (`fk_cargos`) REFERENCES `cargos` (`idCargo`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.familias_plantas
CREATE TABLE IF NOT EXISTS `familias_plantas` (
  `idfamiliaPlanta` int(11) NOT NULL AUTO_INCREMENT,
  `nomFamilia` varchar(45) NOT NULL,
  PRIMARY KEY (`idfamiliaPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para procedimiento bdplantas.gestionar_plantas
DELIMITER //
CREATE PROCEDURE `gestionar_plantas`(
    IN ev INT,
    IN i_idPlanta INT,	
    IN i_nombreCientifico VARCHAR(255),
    IN i_nomFamilia VARCHAR(255),
    IN i_nombresComunes TEXT,
    IN i_urlimagenes TEXT,
    IN i_idEmpleado INT,
    IN i_datoMorfologico TEXT -- NUEVO PARÁMETRO
)
BEGIN
    DECLARE idFamilia INT;
    DECLARE msg_error TEXT;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        GET DIAGNOSTICS CONDITION 1 msg_error = MESSAGE_TEXT;
        SELECT CONCAT('Error: ', msg_error) AS respuesta;
    END;

    START TRANSACTION;

    -- Buscar ID de la familia
    SET idFamilia = (
        SELECT idfamiliaPlanta
        FROM familias_plantas
        WHERE nomFamilia = i_nomFamilia
        LIMIT 1
    );

    CASE ev
        WHEN 1 THEN -- Insertar
            INSERT INTO plantas(nombreCientifico, fk_familiasplantas)
            VALUES (i_nombreCientifico, idFamilia);

            SET @lastPlantId = LAST_INSERT_ID();

            -- Insertar datos morfológicos (relación 1 a 1 con plantas)
            INSERT INTO datos_morfologicos(datoMorfologico, fk_plantas)
            VALUES (i_datoMorfologico, @lastPlantId);

            -- Insertar nombres comunes
            WHILE LOCATE(',', i_nombresComunes) > 0 DO
                INSERT INTO nombres_comunes(nombreComun, fk_plantas)
                VALUES (
                    TRIM(SUBSTRING_INDEX(i_nombresComunes, ',', 1)),
                    @lastPlantId
                );
                SET i_nombresComunes = SUBSTRING(i_nombresComunes FROM LOCATE(',', i_nombresComunes) + 1);
            END WHILE;

            IF TRIM(i_nombresComunes) <> '' THEN
                INSERT INTO nombres_comunes(nombreComun, fk_plantas)
                VALUES (TRIM(i_nombresComunes), @lastPlantId);
            END IF;

            -- Insertar imágenes
            WHILE LOCATE(',', i_urlimagenes) > 0 DO
                INSERT INTO linksimagenes(linkimagen, fk_plantas)
                VALUES (
                    TRIM(SUBSTRING_INDEX(i_urlimagenes, ',', 1)),
                    @lastPlantId
                );
                SET i_urlimagenes = SUBSTRING(i_urlimagenes FROM LOCATE(',', i_urlimagenes) + 1);
            END WHILE;

            IF TRIM(i_urlimagenes) <> '' THEN
                INSERT INTO linksimagenes(linkimagen, fk_plantas)
                VALUES (TRIM(i_urlimagenes), @lastPlantId);
            END IF;

            INSERT INTO plantas_registros (fk_plantas, fk_empleados)
            VALUES (@lastPlantId, i_idEmpleado);

            SELECT 'Planta registrada correctamente' AS respuesta;

        WHEN 2 THEN -- Actualizar
            UPDATE plantas
            SET nombreCientifico = i_nombreCientifico,
                fk_familiasplantas = idFamilia
            WHERE idPlanta = i_idPlanta;

            -- Actualizar datos morfológicos
            UPDATE datos_morfologicos
            SET datoMorfologico = i_datoMorfologico
            WHERE fk_plantas = i_idPlanta;
            
             IF ROW_COUNT() = 0 AND i_datoMorfologico IS NOT NULL AND TRIM(i_datoMorfologico) <> '' THEN
                INSERT INTO datos_morfologicos(datoMorfologico, fk_plantas)
                VALUES (i_datoMorfologico, i_idPlanta);
            END IF;

            -- Borrar nombres anteriores
            DELETE FROM nombres_comunes WHERE fk_plantas = i_idPlanta;

            -- Insertar nuevos nombres comunes
            WHILE LOCATE(',', i_nombresComunes) > 0 DO
                INSERT INTO nombres_comunes(nombreComun, fk_plantas)
                VALUES (
                    TRIM(SUBSTRING_INDEX(i_nombresComunes, ',', 1)),
                    i_idPlanta
                );
                SET i_nombresComunes = SUBSTRING(i_nombresComunes FROM LOCATE(',', i_nombresComunes) + 1);
            END WHILE;

            IF TRIM(i_nombresComunes) <> '' THEN
                INSERT INTO nombres_comunes(nombreComun, fk_plantas)
                VALUES (TRIM(i_nombresComunes), i_idPlanta);
            END IF;

            -- Borrar imágenes anteriores
            DELETE FROM linksimagenes WHERE fk_plantas = i_idPlanta;

            -- Insertar nuevas imágenes
            WHILE LOCATE(',', i_urlimagenes) > 0 DO
                INSERT INTO linksimagenes(linkimagen, fk_plantas)
                VALUES (
                    TRIM(SUBSTRING_INDEX(i_urlimagenes, ',', 1)),
                    i_idPlanta
                );
                SET i_urlimagenes = SUBSTRING(i_urlimagenes FROM LOCATE(',', i_urlimagenes) + 1);
            END WHILE;

            IF TRIM(i_urlimagenes) <> '' THEN
                INSERT INTO linksimagenes(linkimagen, fk_plantas)
                VALUES (TRIM(i_urlimagenes), i_idPlanta);
            END IF;

            IF NOT EXISTS (
                SELECT 1 FROM plantas_registros
                WHERE fk_plantas = i_idPlanta AND fk_empleados = i_idEmpleado
            ) THEN
                INSERT INTO plantas_registros (fk_plantas, fk_empleados)
                VALUES (i_idPlanta, i_idEmpleado);
            END IF;

            SELECT 'Planta actualizada correctamente' AS respuesta;

        WHEN 3 THEN -- Archivar
            SELECT 'Función de archivado aún no implementada' AS respuesta;

        ELSE
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Evento no reconocido. Usa 1 (insertar), 2 (actualizar), 3 (archivar)';
    END CASE;

    COMMIT;
END//
DELIMITER ;

-- Volcando estructura para tabla bdplantas.linksimagenes
CREATE TABLE IF NOT EXISTS `linksimagenes` (
  `idLinksImagenes` int(11) NOT NULL AUTO_INCREMENT,
  `linkImagen` mediumtext NOT NULL,
  `fk_plantas` int(11) NOT NULL,
  PRIMARY KEY (`idLinksImagenes`),
  KEY `fk_linksImagenes_plantas1_idx` (`fk_plantas`),
  CONSTRAINT `fk_linksImagenes_plantas1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=277 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.nombres_comunes
CREATE TABLE IF NOT EXISTS `nombres_comunes` (
  `idNombrecomun` int(11) NOT NULL AUTO_INCREMENT,
  `nombreComun` varchar(40) NOT NULL,
  `fk_plantas` int(11) NOT NULL,
  PRIMARY KEY (`idNombrecomun`),
  KEY `fk_plantas` (`fk_plantas`),
  CONSTRAINT `nombres_comunes_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=278 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para procedimiento bdplantas.obtener_datos_login
DELIMITER //
CREATE PROCEDURE `obtener_datos_login`(
    IN p_usuario VARCHAR(50),
    IN p_contraseña VARCHAR(100)
)
BEGIN
    SELECT 
        u.idUsuario,
        u.usuario,
        e.idEmpleado,
        e.correo,
        p.idPersona,
        p.DNI,
        p.nombres,
        p.apellido1,
        p.apellido2,
        p.telefono,
        p.direccion,
        c.categoria
    FROM usuarios u
    JOIN empleados e ON u.fk_empleados = e.idEmpleado
    JOIN personas p ON e.fk_personas = p.idPersona
    JOIN cargos c ON c.idCargo = e.fk_cargos
    WHERE u.usuario = p_usuario
      AND u.contraseña = SHA1(p_contraseña)
    LIMIT 1;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bdplantas.obtener_datos_usuario
DELIMITER //
CREATE PROCEDURE `obtener_datos_usuario`(
    IN p_usuario VARCHAR(50)
)
BEGIN
    SELECT 
        u.idUsuario,
        u.usuario,
        e.idEmpleado,
        e.correo,
        p.idPersona,
        p.DNI,
        p.nombres,
        p.apellido1,
        p.apellido2,
        p.telefono,
        p.direccion,
        c.categoria
    FROM usuarios u
    JOIN empleados e ON u.fk_empleados = e.idEmpleado
    JOIN personas p ON e.fk_personas = p.idPersona
    JOIN cargos c ON c.idCargo = e.fk_cargos
    WHERE u.usuario = p_usuario
    LIMIT 1;
END//
DELIMITER ;

-- Volcando estructura para tabla bdplantas.personas
CREATE TABLE IF NOT EXISTS `personas` (
  `idPersona` int(11) NOT NULL AUTO_INCREMENT,
  `DNI` varchar(8) NOT NULL,
  `nombres` varchar(50) NOT NULL,
  `apellido1` varchar(45) NOT NULL,
  `apellido2` varchar(45) NOT NULL,
  `telefono` varchar(9) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  PRIMARY KEY (`idPersona`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.plantas
CREATE TABLE IF NOT EXISTS `plantas` (
  `idPlanta` int(11) NOT NULL AUTO_INCREMENT,
  `nombreCientifico` varchar(50) NOT NULL,
  `fk_familiasplantas` int(11) NOT NULL,
  PRIMARY KEY (`idPlanta`),
  UNIQUE KEY `nombreCientifico` (`nombreCientifico`),
  KEY `familiasPlantas_idfamiliasPlantas` (`fk_familiasplantas`),
  CONSTRAINT `plantas_ibfk_1` FOREIGN KEY (`fk_familiasplantas`) REFERENCES `familias_plantas` (`idfamiliaPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.plantas_registros
CREATE TABLE IF NOT EXISTS `plantas_registros` (
  `fk_plantas` int(11) NOT NULL,
  `fk_empleados` int(11) NOT NULL,
  KEY `fk_plantas` (`fk_plantas`),
  KEY `fk_empleados` (`fk_empleados`),
  CONSTRAINT `planta_registro_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`),
  CONSTRAINT `planta_registro_ibfk_2` FOREIGN KEY (`fk_empleados`) REFERENCES `empleados` (`idEmpleado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.provincias
CREATE TABLE IF NOT EXISTS `provincias` (
  `idprovincias` int(11) NOT NULL AUTO_INCREMENT,
  `nombreProvincia` varchar(45) NOT NULL,
  `fk_regiones` int(11) NOT NULL,
  PRIMARY KEY (`idprovincias`),
  KEY `fk_provincias_regiones1_idx` (`fk_regiones`),
  CONSTRAINT `fk_provincias_regiones1` FOREIGN KEY (`fk_regiones`) REFERENCES `regiones` (`idRegion`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.provincia_ecoregion
CREATE TABLE IF NOT EXISTS `provincia_ecoregion` (
  `fk_ecoregiones` int(11) NOT NULL,
  `fk_provincias` int(11) NOT NULL,
  KEY `fk_provincia_ecoregion_ecoregiones1_idx` (`fk_ecoregiones`),
  KEY `fk_provincia_ecoregion_provincias1_idx` (`fk_provincias`),
  CONSTRAINT `fk_provincia_ecoregion_ecoregiones1` FOREIGN KEY (`fk_ecoregiones`) REFERENCES `ecoregiones` (`idecoregion`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_provincia_ecoregion_provincias1` FOREIGN KEY (`fk_provincias`) REFERENCES `provincias` (`idprovincias`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.regiones
CREATE TABLE IF NOT EXISTS `regiones` (
  `idRegion` int(11) NOT NULL AUTO_INCREMENT,
  `region` varchar(50) NOT NULL,
  PRIMARY KEY (`idRegion`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.saberes_culturales
CREATE TABLE IF NOT EXISTS `saberes_culturales` (
  `idSaberes` int(11) NOT NULL AUTO_INCREMENT,
  `descripcionSaber` text NOT NULL,
  `fk_plantas` int(11) NOT NULL,
  PRIMARY KEY (`idSaberes`),
  KEY `fk_plantas` (`fk_plantas`),
  CONSTRAINT `saberesculturales_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para procedimiento bdplantas.sp_obtener_info_completa_planta
DELIMITER //
CREATE PROCEDURE `sp_obtener_info_completa_planta`(IN p_id_planta INT)
BEGIN
    -- Verificar si la planta existe y no está archivada
    SELECT COUNT(*) INTO @planta_existe
    FROM plantas p
    WHERE p.idPlanta = p_id_planta
    AND p.idPlanta NOT IN (SELECT DISTINCT fk_plantas FROM archivacionesplantas);
    
    IF @planta_existe = 0 THEN
        SELECT 'Planta no encontrada o está archivada' AS error;
    ELSE
        SELECT 
            p.idPlanta,
            p.nombreCientifico,
            (SELECT li.linkImagen FROM linksimagenes li WHERE li.fk_plantas = p.idPlanta LIMIT 1) AS linkImagen,
            fp.nomFamilia,
            
            -- Nombres comunes
            (SELECT GROUP_CONCAT(DISTINCT nc.nombreComun SEPARATOR ', ') 
             FROM nombres_comunes nc 
             WHERE nc.fk_plantas = p.idPlanta) AS nombres_comunes,
            
            -- Ecoregiones (solo no archivadas)
            (SELECT GROUP_CONCAT(DISTINCT e.ecoregion SEPARATOR ', ') 
             FROM ecoregion_planta ep
             INNER JOIN ecoregiones e ON ep.fk_ecoregiones = e.idecoregion
             WHERE ep.fk_plantas = p.idPlanta
             AND ep.idecoregion_planta NOT IN (SELECT DISTINCT fk_ecoregion_plantas FROM archivaciones_ubicaciones)) AS ecoregiones,
            
            -- Regiones (solo no archivadas)
            (SELECT GROUP_CONCAT(DISTINCT r.region SEPARATOR ', ') 
             FROM ecoregion_planta ep
             INNER JOIN ecoregiones e ON ep.fk_ecoregiones = e.idecoregion
             INNER JOIN provincia_ecoregion pe ON e.idecoregion = pe.fk_ecoregiones
             INNER JOIN provincias prov ON pe.fk_provincias = prov.idprovincias
             INNER JOIN regiones r ON prov.fk_regiones = r.idRegion
             WHERE ep.fk_plantas = p.idPlanta
             AND ep.idecoregion_planta NOT IN (SELECT DISTINCT fk_ecoregion_plantas FROM archivaciones_ubicaciones)) AS regiones,
            
            -- Provincias (solo no archivadas)
            (SELECT GROUP_CONCAT(DISTINCT prov.nombreProvincia SEPARATOR ', ') 
             FROM ecoregion_planta ep
             INNER JOIN ecoregiones e ON ep.fk_ecoregiones = e.idecoregion
             INNER JOIN provincia_ecoregion pe ON e.idecoregion = pe.fk_ecoregiones
             INNER JOIN provincias prov ON pe.fk_provincias = prov.idprovincias
             WHERE ep.fk_plantas = p.idPlanta
             AND ep.idecoregion_planta NOT IN (SELECT DISTINCT fk_ecoregion_plantas FROM archivaciones_ubicaciones)) AS provincias,
            
            -- Usos medicinales (solo no archivados)
            (SELECT GROUP_CONCAT(
                DISTINCT CONCAT('Parte: ', u.parte, ' | Uso: ', u.uso, ' | Preparación: ', u.preparacion, ' | Contraindicaciones: ', u.contraIndicaciones) 
                SEPARATOR ' || '
             ) 
             FROM usos u 
             WHERE u.fk_plantas = p.idPlanta
             AND u.idUsos NOT IN (SELECT DISTINCT fk_usos FROM archivaciones_usos)) AS usos_medicinales,
            
            -- Saberes culturales (solo no archivados)
            (SELECT GROUP_CONCAT(DISTINCT sc.descripcionSaber SEPARATOR ' || ') 
             FROM saberes_culturales sc 
             WHERE sc.fk_plantas = p.idPlanta
             AND sc.idSaberes NOT IN (SELECT DISTINCT fk_saberes_culturales FROM archivaciones_saberes)) AS saberes_culturales,
            
            -- Aportes de expertos
            (SELECT GROUP_CONCAT(
                DISTINCT CONCAT('Fecha: ', ae.fecha, ' | Descripción: ', ae.descripcion, ' | Experto: ', CONCAT(pe.nombres, ' ', pe.apellido1, ' ', pe.apellido2), ' | Tipo: ', ta.nombreTipo) 
                SEPARATOR ' || '
             ) 
             FROM aportes_expertos ae
             INNER JOIN personas pe ON ae.fk_personas = pe.idPersona
             INNER JOIN tipos_aportes ta ON ae.fk_tipos_aportes = ta.idTipoAporte
             WHERE ae.fk_plantas = p.idPlanta) AS aportes_expertos,
            
            -- Empleado que registró
            (SELECT GROUP_CONCAT(DISTINCT CONCAT(pe.nombres, ' ', pe.apellido1, ' ', pe.apellido2) SEPARATOR ', ') 
             FROM plantas_registros pr
             INNER JOIN empleados emp ON pr.fk_empleados = emp.idEmpleado
             INNER JOIN personas pe ON emp.fk_personas = pe.idPersona
             WHERE pr.fk_plantas = p.idPlanta) AS empleado_registro,
            
            -- Cargo del empleado
            (SELECT GROUP_CONCAT(DISTINCT c.categoria SEPARATOR ', ') 
             FROM plantas_registros pr
             INNER JOIN empleados emp ON pr.fk_empleados = emp.idEmpleado
             INNER JOIN cargos c ON emp.fk_cargos = c.idCargo
             WHERE pr.fk_plantas = p.idPlanta) AS cargo_empleado,
            
            -- Datos morfológicos
            (SELECT GROUP_CONCAT(DISTINCT dm.datoMorfologico SEPARATOR ' || ') 
             FROM datos_morfologicos dm 
             WHERE dm.fk_plantas = p.idPlanta) AS datos_morfologicos
            
        FROM plantas p
        INNER JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
        WHERE p.idPlanta = p_id_planta;
    END IF;
END//
DELIMITER ;

-- Volcando estructura para tabla bdplantas.tipos_aportes
CREATE TABLE IF NOT EXISTS `tipos_aportes` (
  `idTipoAporte` int(11) NOT NULL AUTO_INCREMENT,
  `nombreTipo` varchar(100) NOT NULL,
  PRIMARY KEY (`idTipoAporte`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.ubicaciones_nombres
CREATE TABLE IF NOT EXISTS `ubicaciones_nombres` (
  `fk_nombres_comunes` int(11) NOT NULL,
  `fk_regiones` int(11) NOT NULL,
  KEY `fk_nombres_comunes1_idx` (`fk_nombres_comunes`),
  KEY `fk_ubicaciones_nombres_regiones1_idx` (`fk_regiones`),
  CONSTRAINT `fk_nombres_comunes1` FOREIGN KEY (`fk_nombres_comunes`) REFERENCES `nombres_comunes` (`idNombrecomun`),
  CONSTRAINT `fk_ubicaciones_nombres_regiones1` FOREIGN KEY (`fk_regiones`) REFERENCES `regiones` (`idRegion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.usos
CREATE TABLE IF NOT EXISTS `usos` (
  `idUsos` int(11) NOT NULL AUTO_INCREMENT,
  `parte` varchar(50) NOT NULL,
  `uso` varchar(50) NOT NULL,
  `contraIndicaciones` varchar(80) NOT NULL,
  `preparacion` varchar(80) NOT NULL,
  `fk_plantas` int(11) NOT NULL,
  PRIMARY KEY (`idUsos`),
  KEY `fk_plantas` (`fk_plantas`),
  CONSTRAINT `usos_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla bdplantas.usuarios
CREATE TABLE IF NOT EXISTS `usuarios` (
  `idUsuario` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(45) NOT NULL,
  `contraseña` varchar(40) DEFAULT NULL,
  `fk_empleados` int(11) NOT NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `usuario_UNIQUE` (`usuario`),
  KEY `fk_usuarios_empleados1_idx` (`fk_empleados`),
  CONSTRAINT `fk_usuarios_empleados1` FOREIGN KEY (`fk_empleados`) REFERENCES `empleados` (`idEmpleado`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para función bdplantas.validar_login
DELIMITER //
CREATE FUNCTION `validar_login`(p_usuario VARCHAR(50), p_contraseña VARCHAR(100)) RETURNS int(11)
    DETERMINISTIC
BEGIN
    DECLARE v_id INT;
    

    SELECT idUsuario
    INTO v_id
    FROM usuarios
    WHERE usuario = p_usuario
      AND contraseña = SHA1(p_contraseña)
    LIMIT 1;

    RETURN IFNULL(v_id, 0)
    ;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bdplantas.visor_ecoregiones
DELIMITER //
CREATE PROCEDURE `visor_ecoregiones`()
BEGIN
    select * from ecoregiones;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bdplantas.visor_ecoregion_planta
DELIMITER //
CREATE PROCEDURE `visor_ecoregion_planta`(
    IN ev INT,
    IN i_id INT
)
BEGIN
    CASE ev
        WHEN 1 THEN -- Listar ecoregiones de una planta
            SELECT 
                ep.idecoregion_planta,
                ep.fk_plantas,
                p.nombreCientifico,
                ep.fk_ecoregiones,
                e.ecoregion
            FROM ecoregion_planta ep
            JOIN plantas p ON ep.fk_plantas = p.idPlanta
            JOIN ecoregiones e ON ep.fk_ecoregiones = e.idecoregion
            WHERE ep.fk_plantas = i_id
              AND ep.idecoregion_planta NOT IN (
                  SELECT fk_ecoregion_plantas FROM archivaciones_ubicaciones
              )
            ORDER BY e.ecoregion;
        WHEN 2 THEN -- Listar plantas de una ecoregión
            SELECT 
                ep.idecoregion_planta,
                ep.fk_plantas,
                p.nombreCientifico,
                fp.nomFamilia,
                ep.fk_ecoregiones,
                e.ecoregion
            FROM ecoregion_planta ep
            JOIN plantas p ON ep.fk_plantas = p.idPlanta
            JOIN familias_plantas fp ON p.fk_familiasplantas = fp.idfamiliaPlanta
            JOIN ecoregiones e ON ep.fk_ecoregiones = e.idecoregion
            WHERE ep.fk_ecoregiones = i_id
              AND ep.idecoregion_planta NOT IN (
                  SELECT fk_ecoregion_plantas FROM archivaciones_ubicaciones
              )
              AND p.idPlanta NOT IN (
                  SELECT fk_plantas FROM archivacionesplantas
              )
            ORDER BY p.nombreCientifico;
        ELSE
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Evento no reconocido. Usa 1 (por planta), 2 (por ecoregión)';
    END CASE;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bdplantas.visor_provincias_por_region
DELIMITER //
CREATE PROCEDURE `visor_provincias_por_region`(
    IN i_idRegion INT
)
BEGIN
    SELECT 
        p.idprovincias,
        p.nombreProvincia,
        p.fk_regiones,
        r.region
    FROM provincias p
    JOIN regiones r ON p.fk_regiones = r.idRegion
    WHERE p.fk_regiones = i_idRegion
    ORDER BY p.nombreProvincia;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bdplantas.visor_provincia_ecoregion
DELIMITER //
CREATE PROCEDURE `visor_provincia_ecoregion`(
    IN i_id INT
)
BEGIN
    SELECT 
        e.idecoregion,
        e.ecoregion,
        p.idprovincias,
        r.idRegion
    FROM provincia_ecoregion pe
    JOIN ecoregiones e ON pe.fk_ecoregiones = e.idecoregion
    JOIN provincias p ON pe.fk_provincias = p.idprovincias
    JOIN regiones r ON p.fk_regiones = r.idRegion
    WHERE pe.fk_provincias = i_id
    ORDER BY e.ecoregion;
END//
DELIMITER ;

-- Volcando estructura para procedimiento bdplantas.visor_regiones
DELIMITER //
CREATE PROCEDURE `visor_regiones`()
BEGIN
    SELECT idRegion, region FROM regiones ORDER BY region;
END//
DELIMITER ;

-- Volcando estructura para vista bdplantas.vta_plantas2
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `vta_plantas2` (
	`idPlanta` INT(11) NOT NULL,
	`nombreCientifico` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_unicode_ci',
	`Imagenes` MEDIUMTEXT NULL COLLATE 'latin1_swedish_ci',
	`nomFamilia` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_unicode_ci',
	`nombres_comunes` MEDIUMTEXT NULL COLLATE 'utf8mb4_unicode_ci',
	`descMorfologica` MEDIUMTEXT NULL COLLATE 'utf8mb4_unicode_ci'
) ENGINE=MyISAM;

-- Volcando estructura para vista bdplantas.vta_plantas_activas
-- Creando tabla temporal para superar errores de dependencia de VIEW
CREATE TABLE `vta_plantas_activas` (
	`idPlanta` INT(11) NOT NULL,
	`nombreCientifico` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_unicode_ci',
	`linkImagen` MEDIUMTEXT NULL COLLATE 'latin1_swedish_ci',
	`nomFamilia` VARCHAR(1) NOT NULL COLLATE 'utf8mb4_unicode_ci',
	`nombres_comunes` MEDIUMTEXT NULL COLLATE 'utf8mb4_unicode_ci'
) ENGINE=MyISAM;

-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `vta_plantas2`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vta_plantas2` AS select `p`.`idPlanta` AS `idPlanta`,`p`.`nombreCientifico` AS `nombreCientifico`,(select group_concat(distinct `li`.`linkImagen` separator ', ') from `linksimagenes` `li` where `li`.`fk_plantas` = `p`.`idPlanta`) AS `Imagenes`,`fp`.`nomFamilia` AS `nomFamilia`,group_concat(distinct `nc`.`nombreComun` separator ', ') AS `nombres_comunes`,(select group_concat(distinct `dm`.`datoMorfologico` separator ', ') from `datos_morfologicos` `dm` where `dm`.`fk_plantas` = `p`.`idPlanta`) AS `descMorfologica` from (((`plantas` `p` join `familias_plantas` `fp` on(`p`.`fk_familiasplantas` = `fp`.`idfamiliaPlanta`)) left join `nombres_comunes` `nc` on(`p`.`idPlanta` = `nc`.`fk_plantas`)) left join `datos_morfologicos` `dm` on(`p`.`idPlanta` = `dm`.`fk_plantas`)) where `p`.`idPlanta` in (select distinct `archivacionesplantas`.`fk_plantas` from `archivacionesplantas`) is false group by `p`.`idPlanta`,`p`.`nombreCientifico`,`fp`.`nomFamilia`
;

-- Eliminando tabla temporal y crear estructura final de VIEW
DROP TABLE IF EXISTS `vta_plantas_activas`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `vta_plantas_activas` AS select `p`.`idPlanta` AS `idPlanta`,`p`.`nombreCientifico` AS `nombreCientifico`,(select `li`.`linkImagen` from `linksimagenes` `li` where `li`.`fk_plantas` = `p`.`idPlanta` limit 1) AS `linkImagen`,`fp`.`nomFamilia` AS `nomFamilia`,group_concat(distinct `nc`.`nombreComun` separator ', ') AS `nombres_comunes` from ((`plantas` `p` join `familias_plantas` `fp` on(`p`.`fk_familiasplantas` = `fp`.`idfamiliaPlanta`)) left join `nombres_comunes` `nc` on(`p`.`idPlanta` = `nc`.`fk_plantas`)) where `p`.`idPlanta` in (select distinct `archivacionesplantas`.`fk_plantas` from `archivacionesplantas`) is false group by `p`.`idPlanta`,`p`.`nombreCientifico`,`fp`.`nomFamilia`
;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
