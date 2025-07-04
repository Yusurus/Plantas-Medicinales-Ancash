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

-- Volcando datos para la tabla bdplantas.aportes_expertos: ~10 rows (aproximadamente)
INSERT INTO `aportes_expertos` (`idAporteExperto`, `fecha`, `descripcion`, `fk_personas`, `fk_plantas`, `fk_tipos_aportes`) VALUES
	(1, '2024-01-15', 'La manzanilla de Ancash tiene mayor concentración de aceites esenciales que otras variedades', 7, 1, 1),
	(2, '2024-01-20', 'Se recomienda recolectar las flores en las primeras horas de la mañana', 8, 1, 4),
	(3, '2024-02-10', 'La menta crece mejor en las quebradas húmedas de la Cordillera Blanca', 9, 2, 3),
	(4, '2024-02-15', 'Método tradicional de secado en sombra para conservar propiedades', 10, 2, 2),
	(5, '2024-03-05', 'Rosa mosqueta abundante en altitudes entre 3000-3800 msnm en Ancash', 7, 3, 3),
	(6, '2024-03-12', 'Las papas nativas tienen propiedades antiinflamatorias únicas', 8, 4, 1),
	(7, '2024-04-01', 'Manayupa efectiva para problemas renales según estudios locales', 9, 5, 1),
	(8, '2024-04-08', 'Llantén muy común en caminos de herradura de toda la región', 10, 6, 3),
	(9, '2024-05-03', 'Malva útil para problemas respiratorios en clima frío de altura', 7, 7, 1),
	(10, '2024-05-10', 'Hinojo cultivado tradicionalmente en huertos familiares ancashinos', 8, 8, 8);

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

-- Volcando datos para la tabla bdplantas.archivacionesplantas: ~2 rows (aproximadamente)
INSERT INTO `archivacionesplantas` (`idArchivaPlanta`, `fecha`, `motivo`, `fk_plantas`, `fk_empleados`) VALUES
	(1, '2024-06-01', 'Planta ya no encontrada en ubicación original registrada', 1, 1),
	(2, '2024-06-15', 'Información duplicada con otro registro', 11, 2);

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

-- Volcando datos para la tabla bdplantas.archivaciones_saberes: ~2 rows (aproximadamente)
INSERT INTO `archivaciones_saberes` (`idArchivaSaber`, `fechaArchivaSaber`, `motivoArchivaSaber`, `fk_saberes_culturales`, `fk_empleados`) VALUES
	(1, '2024-07-01', 'Información no verificada por comunidad local', 1, 3),
	(2, '2024-07-10', 'Práctica ya no utilizada en la región', 5, 4);

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

-- Volcando datos para la tabla bdplantas.archivaciones_ubicaciones: ~0 rows (aproximadamente)

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

-- Volcando datos para la tabla bdplantas.archivaciones_usos: ~2 rows (aproximadamente)
INSERT INTO `archivaciones_usos` (`idArchivaUso`, `fecha`, `motivo`, `fk_usos`, `fk_empleados`) VALUES
	(1, '2024-09-01', 'Contraindicación no confirmada científicamente', 1, 1),
	(2, '2024-09-10', 'Método de preparación actualizado', 8, 2);

-- Volcando estructura para tabla bdplantas.cargos
CREATE TABLE IF NOT EXISTS `cargos` (
  `idCargo` int(11) NOT NULL AUTO_INCREMENT,
  `categoria` varchar(50) NOT NULL,
  `salario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idCargo`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla bdplantas.cargos: ~6 rows (aproximadamente)
INSERT INTO `cargos` (`idCargo`, `categoria`, `salario`) VALUES
	(1, 'Botánico Senior', 3500.00),
	(2, 'Etnobotánico', 3200.00),
	(3, 'Investigador Junior', 2800.00),
	(4, 'Curador de Herbario', 3000.00),
	(5, 'Técnico de Campo', 2500.00),
	(6, 'Administrador BD', 3300.00);

-- Volcando estructura para tabla bdplantas.datos_morfologicos
CREATE TABLE IF NOT EXISTS `datos_morfologicos` (
  `idDatomorfologico` int(11) NOT NULL AUTO_INCREMENT,
  `datoMorfologico` text NOT NULL,
  `fk_plantas` int(11) NOT NULL,
  PRIMARY KEY (`idDatomorfologico`),
  KEY `fk_plantas` (`fk_plantas`),
  CONSTRAINT `datosmorfologicos_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla bdplantas.datos_morfologicos: ~50 rows (aproximadamente)
INSERT INTO `datos_morfologicos` (`idDatomorfologico`, `datoMorfologico`, `fk_plantas`) VALUES
	(1, 'Hierba anual de 20-60 cm de altura. Tallos erectos, ramificados, glabros. Hojas alternas, bipinnatipartidas, segmentos lineares. Capítulos solitarios de 1-2 cm de diámetro, pedúnculo largo. Flores liguladas blancas, reflexas; flores del disco amarillas, tubulares. Receptáculo cónico, hueco. Aquenios pequeños, sin vilano.', 1),
	(2, 'Hierba perenne de 30-90 cm de altura. Tallos cuadrangulares, erectos, ramificados, glabros o ligeramente pubescentes. Hojas opuestas, ovadas a lanceoladas, de 4-9 cm, margen aserrado, pecioladas. Inflorescencias en espigas terminales densas de 5-10 cm. Flores pequeñas, rosadas o púrpuras, cáliz tubular con 5 dientes. Fruto en núculas.', 2),
	(3, 'Arbusto espinoso de 1-3 m de altura. Tallos arqueados con espinas curvas, fuertes. Hojas compuestas, imparipinnadas, 5-9 folíolos ovales, margen doblemente aserrado, envés glanduloso-aromático. Flores solitarias o en grupos de 2-3, de 3-4 cm de diámetro, pétalos rosados. Fruto hipantio ovoide, rojo-anaranjado, de 1-2 cm.', 3),
	(4, 'Hierba perenne de 60-100 cm de altura. Tallos herbáceos, erectos, angulosos. Hojas compuestas, imparipinnadas, folíolos ovales de tamaños variables, algunos intercalares pequeños. Inflorescencias cimosas terminales. Flores de 2-3 cm, corola rotácea, blanca, rosada o violácea. Fruto baya globosa verde. Tubérculos subterráneos variables en forma y color.', 4),
	(5, 'Hierba perenne rastrera de 20-40 cm de altura. Tallos postrados, pubescentes. Hojas trifolioladas, folíolos obovados de 1-3 cm, envés plateado-pubescente. Inflorescencias racemosas axilares. Flores pequeñas de 4-6 mm, rosadas o púrpuras. Fruto lomento articulado, segmentos adherentes, cubierto de pelos ganchudos.', 5),
	(6, 'Hierba perenne acaule de 10-50 cm de altura. Hojas en roseta basal, ovadas a elípticas, de 5-20 cm, 3-9 nervios paralelos prominentes, pecíolo acanalado. Inflorescencias en espigas cilíndricas densas de 5-25 cm, pedúnculo largo. Flores pequeñas, hermafroditas, cáliz 4-partido, corola blanquecina. Fruto cápsula que se abre transversalmente.', 6),
	(7, 'Hierba bienal o perenne de 50-120 cm de altura. Tallos erectos o ascendentes, ramificados, pubescentes. Hojas alternas, palmatífidas con 5-7 lóbulos, margen crenado-dentado, largamente pecioladas. Flores axilares agrupadas, de 2-4 cm de diámetro, pétalos obcordados, rosado-púrpuras con venas más oscuras. Fruto esquizocarpo circular, mericarpos reticulados.', 7),
	(8, 'Hierba perenne de 1-2.5 m de altura. Tallos erectos, estriados, ramificados en la parte superior, glabros. Hojas alternas, 3-4 veces pinnaticompuestas, segmentos filiformes aromáticos. Inflorescencias en umbelas compuestas terminales de 5-15 cm de diámetro. Flores pequeñas amarillas. Frutos diaquenios oblongos, costados, aromáticos.', 8),
	(9, 'Hierba anual postrada de 10-40 cm de altura. Tallos rojizos, densamente pilosos, con látex blanco. Hojas opuestas, ovadas a oblongas, de 1-3 cm, margen finamente aserrado, asimétricas en la base, pilosas. Inflorescencias en ciatios axilares agrupados. Flores pequeñas, sin perianto. Fruto cápsula trilocular pilosa. Semillas pequeñas, rugosas, rosadas.', 9),
	(10, 'Hierba perenne de 5-20 cm de altura. Tallos postrados o ascendentes, pubescentes. Hojas palmatífidas con 5-7 segmentos profundos, margen inciso-dentado, largamente pecioladas, pubescentes. Flores solitarias o en pares, pétalos blancos o rosados de 6-10 mm, obovados. Fruto esquizocarpo con rostro largo, mericarpos con arista plumosa.', 10),
	(11, 'Arbusto de 1-3 m de altura. Tallos erectos, ramificados, corteza gris-pardusca. Hojas alternas, ovadas a lanceoladas, de 3-8 cm, margen irregularmente dentado, subsésiles, coriáceas. Inflorescencias en panículas terminales densas. Capítulos pequeños, unisexuales (planta dioica), flores tubulares blanquecinas. Aquenios pequeños con vilano blanco abundante.', 11),
	(12, 'Hierba perenne aromática de 20-50 cm de altura. Tallos cuadrangulares, erectos, ramificados, pubescentes. Hojas opuestas, ovadas, de 0.5-2 cm, margen entero o ligeramente crenado, densamente glanduloso-pubescentes, muy aromáticas. Inflorescencias en verticilastros axilares densos. Flores pequeñas, rosadas o púrpuras, cáliz bilabiado. Fruto en núculas pequeñas.', 12),
	(13, 'Arbusto sarmentoso de 1-2 m de altura. Tallos arqueados, con espinas pequeñas curvas. Hojas alternas, compuestas, 3-5 folíolos ovados, margen aserrado, envés blanquecino-tomentoso. Inflorescencias racemosas terminales. Flores de 1-2 cm de diámetro, pétalos blancos o rosados. Fruto agregado (polidrupa) rojizo-anaranjado, comestible, de sabor agridulce.', 13),
	(14, 'Arbusto perenne de 1-3 m de altura. Tallos leñosos en la base, ramificados, pubescentes. Hojas alternas, ovadas a lanceoladas, de 5-12 cm, margen entero, pecioladas, pubescentes en ambas caras. Flores solitarias axilares, péndulas, corola rotácea púrpura con centro blanco. Fruto baya carnosa, globosa a ovoide, roja, amarilla o anaranjada, muy picante.', 14),
	(15, 'Hierba anual erecta de 1-3 m de altura. Tallos robustos, ramificados, pubescentes. Hojas alternas, palmaticompuestas, 7-9 folíolos oblanceolados, de 3-6 cm, pubescentes, pecíolo largo. Inflorescencias en racimos terminales erectos de 15-50 cm. Flores papilionáceas grandes, azules, púrpuras, rosadas o blancas, vistosas. Fruto legumbre de 5-12 cm, pubescente, con 3-8 semillas grandes.', 15),
	(16, 'Tallos huecos, articulados y estriados longitudinalmente, con nudos marcados donde se encuentran las hojas reducidas a vainas', 48),
	(17, 'En efecto, es una planta.', 31),
	(18, 'En efecto, es una planta.', 31),
	(19, 'En efecto, es una planta.', 31),
	(20, 'En efecto, es una planta.', 31),
	(22, 'En efecto, es una planta.', 31),
	(23, 'En efecto, es una planta.', 31),
	(24, 'En efecto, es una planta.', 31),
	(25, 'En efecto, es una planta.', 31),
	(26, 'En efecto, es una planta.', 31),
	(27, 'En efecto, es una planta.', 31),
	(28, 'En efecto, es una planta.', 31),
	(29, 'En efecto, es una planta.', 31),
	(30, 'En efecto, es una planta.', 31),
	(31, 'En efecto, es una planta.', 31),
	(32, 'En efecto, es una planta.', 31),
	(33, 'En efecto, es anís.', 52),
	(36, 'Si, es ajenjo.', 24),
	(38, 'Tamaño: De 60 cm a 2 m de alto.\r\nTallo: Erecto, cuadrado, con estípulas de 5 a 15 mm de largo .\r\nHojas: Lanceoladas a ovadas, de 5 a 15 cm de largo, ápice atenuado, borde aserrado, base cuneada a redondeada; pecíolos de 1 a 3 cm de largo Inflorescencia: Axilares en forma de espigas ramificadas, agrupadas por varias generalmente más largas que el pecíolo.\r\nFlores: Dioicas, pequeñas y de color verde; las masculinas con un perianto de 4 segmentos y 4 estambres, las femeninas con un perianto de 4 partes.\r\nFrutos y semillas: El fruto es un aquenio, ovoide, de 1 a 2 mm de largo, generalmente dispersado entre el perianto, comprimido, color café, café oscuro o café amarillento.\r\nPlántulas: Hipocótilo alargado, de 5 a 8 mm; cotiledones de lámina ovada, ápice retuso, borde entero; epicótilo cilíndrico de hasta 2 mm; hojas opuestas, pecioladas, de lámina aovada a estrechamente elíptica, de 2 a 4 mm de largo y 1 a 2 mm de ancho, borde crenado, con pelos (Espinosa y Sarukhán, 1997).\r\nRaíz: Tiene rizomas.\r\nCaracterísticas especiales: Planta cubierta con pelos urticantess.', 54),
	(39, 'Hojas juveniles opuestas al principio, luego alternas; anchas y lanceoladas. La textura de las hojas es lisa y no glauca, de color verde opaco a verde azulado. Flores bastante insignificantes, blancas o cremosas, 7-11 sostenidas en umbelas axilares.', 28),
	(40, 'Ruta', 55),
	(41, 'Hierba Luisa', 21),
	(44, 'Cartucho', 27),
	(45, 'Ruta', 55),
	(48, 'Hierba Luisa', 21),
	(49, 'Hierba Luisa', 21),
	(50, 'Hierba Luisa', 21),
	(53, 'Tallos huecos, articulados y estriados longitudinalmente, con nudos marcados donde se encuentran las hojas reducidas a vainas', 48),
	(54, 'Alcanza el metro de altura. Es tolerante a la sequía y crece rápidamente, Cenchrus setaceus es una planta muy territorial, si se encuentra cerca de otra planta empezara a competir por el agua y nutrientes.\r\nEl color de las hojas pueden ser verdes, púrpuras o rojas.', 67),
	(55, '¿Cómo puede una sola planta crecer y producir tantos guisantes tan rápidamente? Peashooter dice: «El trabajo duro, el compromiso y un desayuno saludable y equilibrado a base de luz solar y dióxido de carbono rico en fibra lo hacen posible».', 68),
	(56, 'en efecto es una planta 123456789', 20),
	(57, 'Cactus', 69),
	(58, 'en efecto es una planta 123456789', 20),
	(59, '¡Guau!" ladra Rabo de gato "Grrr... ¡Guau, guau! ¿Qué? ¿Confundido? Esperarabas que hiciera "miauuu" solo porque en mi nombre pone "Gato"... y porque parezco un gato también. ¡Pues no! Me niego a que me encasillen de esa manera.', 70),
	(61, 'Hierba perenne de 30-90 cm de altura. Tallos cuadrangulares, erectos, ramificados, glabros o ligeramente pubescentes. Hojas opuestas, ovadas a lanceoladas, de 4-9 cm, margen aserrado, pecioladas. Inflorescencias en espigas terminales densas de 5-10 cm. Flores pequeñas, rosadas o púrpuras, cáliz tubular con 5 dientes. Fruto en núculas.', 2);

-- Volcando estructura para tabla bdplantas.ecoregiones
CREATE TABLE IF NOT EXISTS `ecoregiones` (
  `idecoregion` int(11) NOT NULL AUTO_INCREMENT,
  `ecoregion` varchar(45) NOT NULL,
  PRIMARY KEY (`idecoregion`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla bdplantas.ecoregiones: ~11 rows (aproximadamente)
INSERT INTO `ecoregiones` (`idecoregion`, `ecoregion`) VALUES
	(1, 'Mar Tropical'),
	(2, 'Mar Frío'),
	(3, 'Desierto del Pacífico'),
	(4, 'Bosque Seco Ecuatorial'),
	(5, 'Bosque Tropical del Pacífico'),
	(6, 'Serranía Esteparia'),
	(7, 'Puna'),
	(8, 'Páramo'),
	(9, 'Selva Alta'),
	(10, 'Selva Baja'),
	(11, 'Sabana de Palmeras');

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla bdplantas.ecoregion_planta: ~0 rows (aproximadamente)

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

-- Volcando datos para la tabla bdplantas.empleados: ~6 rows (aproximadamente)
INSERT INTO `empleados` (`idEmpleado`, `correo`, `fk_personas`, `fk_cargos`) VALUES
	(1, 'carlos.rodriguez@plantasancash.pe', 1, 1),
	(2, 'maria.morales@plantasancash.pe', 2, 2),
	(3, 'jose.huaman@plantasancash.pe', 3, 3),
	(4, 'ana.mejia@plantasancash.pe', 4, 4),
	(5, 'pedro.albornoz@plantasancash.pe', 5, 5),
	(6, 'carmen.flores@plantasancash.pe', 6, 6);

-- Volcando estructura para tabla bdplantas.familias_plantas
CREATE TABLE IF NOT EXISTS `familias_plantas` (
  `idfamiliaPlanta` int(11) NOT NULL AUTO_INCREMENT,
  `nomFamilia` varchar(45) NOT NULL,
  PRIMARY KEY (`idfamiliaPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla bdplantas.familias_plantas: ~20 rows (aproximadamente)
INSERT INTO `familias_plantas` (`idfamiliaPlanta`, `nomFamilia`) VALUES
	(1, 'Asteraceae'),
	(2, 'Lamiaceae'),
	(3, 'Rosaceae'),
	(4, 'Solanaceae'),
	(5, 'Fabaceae'),
	(6, 'Plantaginaceae'),
	(7, 'Malvaceae'),
	(8, 'Apiaceae'),
	(9, 'Euphorbiaceae'),
	(10, 'Geraniaceae'),
	(11, 'Verbenaceae'),
	(12, 'Nymphaeaceae'),
	(13, 'Amaryllidaceae'),
	(14, 'Araceae'),
	(15, 'Asphodelaceae'),
	(16, 'Myrtaceae'),
	(17, 'Amaranthaceae'),
	(18, 'Oleaceae'),
	(19, 'Piperaceae'),
	(20, 'Erythroxylaceae'),
	(21, 'Equisetaceae'),
	(22, 'Caprifoliaceae'),
	(23, 'Urticaceae'),
	(24, 'Rutaceae'),
	(25, 'Poaceae'),
	(26, 'Cactaceae'),
	(27, 'Typhaceae');

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
) ENGINE=InnoDB AUTO_INCREMENT=273 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Volcando datos para la tabla bdplantas.linksimagenes: ~93 rows (aproximadamente)
INSERT INTO `linksimagenes` (`idLinksImagenes`, `linkImagen`, `fk_plantas`) VALUES
	(1, 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTuzSCCbhGuXz0ho2AtwXon5XTOw1CDkdhzYkhERxcMae1pV5k1CcixvUShCVtSulmHxGUygE8kqENtfYBXYku0qQ', 1),
	(3, 'https://www.trevorwhiteroses.co.uk/wp-content/uploads/2018/02/Rosa-rubiginosa-amy-robstart-species-rose.jpg', 3),
	(4, 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/S._tuberosum-5.JPG/500px-S._tuberosum-5.JPG', 4),
	(5, 'https://www.algemica.com/web/image/8965/desmodium-2.jpg?access_token=10ce110c-fdd2-4e23-99d0-34d24e4b4b7f', 5),
	(6, 'https://m.media-amazon.com/images/I/61rSPQMt9EL._AC_UF894,1000_QL80_.jpg', 6),
	(7, 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Mallow_January_2008-1.jpg/1200px-Mallow_January_2008-1.jpg', 7),
	(8, 'https://plantasflores.com/wp-content/uploads/2024/09/Foeniculum-vulgare.webp', 8),
	(9, 'https://portal.wiktrop.org/files-api/api/get/crop/img//Euphorbia%20hirta/ephhi_20120201_151612.jpg?h=500', 9),
	(10, 'https://www.chileflora.com/Florachilena/ImagesHigh/IMG_3648.jpg', 10),
	(11, 'https://cloudfront-us-east-1.images.arcpublishing.com/infobae/UGKMUTXRGZDYZMVYWZBBLD4LK4.png', 11),
	(12, 'https://inaturalist-open-data.s3.amazonaws.com/photos/261661343/large.jpeg', 12),
	(13, 'https://upload.wikimedia.org/wikipedia/commons/5/50/Rubus_Roseus_-_Flickr_-_Dick_Culbert.jpg', 13),
	(14, 'https://fm-digital-assets.fieldmuseum.org/1511/600/SOLA_caps_pube_per_22552.jpg', 14),
	(15, 'https://upload.wikimedia.org/wikipedia/commons/8/83/Peruvian_Field_Lupines.jpg', 15),
	(28, 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/20150606Verbena_officinalis1.jpg/960px-20150606Verbena_officinalis1.jpg', 22),
	(29, 'https://bs.plantnet.org/image/m/2f7cc6a3f582c3edc2854280deaef9a17876f9a2', 23),
	(35, 'https://upload.wikimedia.org/wikipedia/commons/8/85/CliviaMiniata.jpg', 26),
	(36, 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Clivia_%28Clivia_miniata%29%2C_jard%C3%ADn_bot%C3%A1nico_de_Tallinn%2C_Estonia%2C_2012-08-13%2C_DD_01.JPG', 26),
	(37, 'https://upload.wikimedia.org/wikipedia/commons/0/0b/Clivia_miniata1.jpg', 26),
	(38, 'https://upload.wikimedia.org/wikipedia/commons/6/64/Clivia_miniata2.jpg', 26),
	(39, 'https://upload.wikimedia.org/wikipedia/commons/8/81/Clivia_miniata_variegata.jpg', 26),
	(50, 'https://bs.plantnet.org/image/m/cbc4da2643362af491edda624973bccf217b3bc3', 29),
	(51, 'https://bs.plantnet.org/image/m/a00340c5ae274d1250514116a5e076869569a782', 29),
	(52, 'https://bs.plantnet.org/image/m/fdff75494c2af50f5871d34398ea843e7c70c979', 29),
	(53, 'https://bs.plantnet.org/image/m/cfad72c34d115e60192c4ac9dfc2a6e7794a984e', 29),
	(54, 'https://bs.plantnet.org/image/m/3e98b4e34aec5890af58460669347f93b6284e34', 29),
	(55, 'https://bs.plantnet.org/image/m/2cba7f53c0f53b193e5a92cbff414c383d511364', 30),
	(56, 'https://bs.plantnet.org/image/m/b0cdc18972fe2254067f7b71a5fbdbc8c511f805', 30),
	(57, 'https://bs.plantnet.org/image/m/1ac1fae12f59ed10f5b6a38af30ef7630e0d87c6', 30),
	(58, 'https://bs.plantnet.org/image/m/05f4a17313437eefce3ac3c1345d173c60716dc0', 30),
	(59, 'https://bs.plantnet.org/image/m/78df2947883ef21aabdc9605396145b596d7db5e', 30),
	(64, 'https://upload.wikimedia.org/wikipedia/commons/2/26/Piper_angustifolium_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-243.jpg', 32),
	(65, 'https://upload.wikimedia.org/wikipedia/commons/2/26/Starr_021122-0021_Piper_aduncum.jpg', 32),
	(66, 'https://upload.wikimedia.org/wikipedia/commons/8/85/Starr_021122-0049_Piper_aduncum.jpg', 32),
	(67, 'https://upload.wikimedia.org/wikipedia/commons/4/42/Starr_040301-0248_Piper_aduncum.jpg', 32),
	(68, 'https://bs.plantnet.org/image/m/7aebc3443a4a583cec896d1961ae8a3d97fd51e3', 44),
	(69, 'https://bs.plantnet.org/image/m/f02a1fcb1af365ff7e6e13ef5080132091660253', 44),
	(70, 'https://bs.plantnet.org/image/m/9b641cd12a620998f850a761b889df3640dd41c2', 44),
	(71, 'https://bs.plantnet.org/image/m/44cd30a7e296159d131ddd7c33d07df60d854219', 44),
	(132, 'https://upload.wikimedia.org/wikipedia/commons/0/0d/Dysphania_ambrosioides_MHNT.BOT.2012.10.16.jpg', 31),
	(133, 'https://upload.wikimedia.org/wikipedia/commons/4/4d/Dysphania_ambrosioides_NRCS-1.jpg', 31),
	(134, 'https://upload.wikimedia.org/wikipedia/commons/7/71/Dysphania_ambrosioides_-_Flickr_-_Kevin_Thiele.jpg', 31),
	(135, 'https://upload.wikimedia.org/wikipedia/commons/a/ac/Dysphania_ambrosioides_Blanco1.69.jpg', 31),
	(136, 'https://upload.wikimedia.org/wikipedia/commons/4/49/Gardenology.org-IMG_2834_rbgs11jan.jpg', 52),
	(137, 'https://upload.wikimedia.org/wikipedia/commons/3/3b/Koehler1887-PimpinellaAnisum.jpg', 52),
	(138, 'https://bs.plantnet.org/image/m/00621823a4bd0a25ca4289dc8a85064c8848629e', 24),
	(139, 'https://bs.plantnet.org/image/m/8fce782100d98a3e90444d11ada6b92f21733300', 24),
	(140, 'https://bs.plantnet.org/image/m/9251dfee9710c7db80ca434fc9eec454a5245df8', 24),
	(141, 'https://bs.plantnet.org/image/m/949798ea781cd902badb912e8be7cfb321652ccc', 24),
	(142, 'https://bs.plantnet.org/image/m/d152495f13e4dc6821783fc20efc5fce08e70132', 24),
	(146, 'https://upload.wikimedia.org/wikipedia/commons/1/16/Brennnessel_1.JPG', 54),
	(147, 'https://upload.wikimedia.org/wikipedia/commons/8/81/Brennhaare.jpg', 54),
	(148, 'https://upload.wikimedia.org/wikipedia/commons/d/da/Brennnessel.jpg', 54),
	(159, 'https://bs.plantnet.org/image/m/2d0e847c46b0762fd16e7dda6a75fbd9ff742955', 28),
	(160, 'https://bs.plantnet.org/image/m/743169c6c3c907fd756697dc8844059b8c219c68', 28),
	(161, 'https://bs.plantnet.org/image/m/956e313ec867f54f26266e598d08bd426e20cd5e', 28),
	(162, 'https://bs.plantnet.org/image/m/9dc678259524092d749022d3954b64f398549b1b', 28),
	(163, 'https://bs.plantnet.org/image/m/ff60c51dd3f385365725e8a2a43ec21f7d3e91f4', 28),
	(178, 'https://upload.wikimedia.org/wikipedia/commons/3/3d/Ruta_graveolens_-_K%C3%B6hler%E2%80%93s_Medizinal-Pflanzen-259.jpg', 55),
	(189, 'https://upload.wikimedia.org/wikipedia/commons/0/01/Aloysia_citrodora_-_leaf.JPG', 21),
	(190, 'https://upload.wikimedia.org/wikipedia/commons/6/6c/Aloysia_citrodora_001.JPG', 21),
	(191, 'https://upload.wikimedia.org/wikipedia/commons/7/70/Aloysia_citrodora_-_flowers.jpg', 21),
	(192, 'https://upload.wikimedia.org/wikipedia/commons/a/a6/Aloysia_citriodora_002.jpg', 21),
	(193, 'https://upload.wikimedia.org/wikipedia/commons/b/b3/Aloysia_citrodora_1.JPG', 21),
	(197, 'https://upload.wikimedia.org/wikipedia/commons/4/49/Pennisetum_setaceum-Guinther.jpg', 67),
	(198, 'https://upload.wikimedia.org/wikipedia/commons/5/52/Pennisetum_setaceum3.jpg', 67),
	(199, 'https://upload.wikimedia.org/wikipedia/commons/c/cc/Purple_Fountain_Grass_%28Pennisetum_setaceum%29_in_Hyderabad%2C_AP_W_IMG_7795.jpg', 67),
	(200, 'https://upload.wikimedia.org/wikipedia/commons/7/72/Purple_Fountain_Grass_%28Pennisetum_setaceum%29_in_Hyderabad%2C_AP_W_IMG_7797.jpg', 67),
	(201, 'https://m.media-amazon.com/images/I/51qXTaqhRTL._AC_SL1000_.jpg', 68),
	(221, 'https://upload.wikimedia.org/wikipedia/commons/9/95/Curtis%27s_botanical_magazine_%28Plate_3079%29_%288411493246%29.jpg', 69),
	(222, 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Rhipsalis_baccifera_2017-09-28_5309.jpg', 69),
	(230, 'https://bs.plantnet.org/image/m/08267707afa960cf9edffcfb0b2c992c4843b942', 27),
	(231, 'https://bs.plantnet.org/image/m/16443eb012a2552f438cd2482b505187b0db48e8', 27),
	(232, 'https://bs.plantnet.org/image/m/63fe7cefb68e2820d36764bd56384520e7561f89', 27),
	(233, 'https://bs.plantnet.org/image/m/bd3bb609bce2c39063f2be32da06af4a7d4497fe', 27),
	(234, 'https://bs.plantnet.org/image/m/e0683f5b95d9b3ec4bebd34a412e9625b5ff5ae2', 27),
	(238, 'https://upload.wikimedia.org/wikipedia/commons/0/0d/Equisetum_arvense_strobili.jpg', 48),
	(239, 'https://upload.wikimedia.org/wikipedia/commons/2/23/Equisetum_arvense_foliage.jpg', 48),
	(240, 'https://upload.wikimedia.org/wikipedia/commons/c/c2/Pr%C3%AAle1.2.JPG', 48),
	(251, 'https://upload.wikimedia.org/wikipedia/commons/e/e3/Typha_flwrs.jpg', 70),
	(252, 'https://upload.wikimedia.org/wikipedia/commons/1/16/Typha_latifolia_02_bgiu.jpg', 70),
	(253, 'https://pm1.aminoapps.com/7345/a0ac5cae9700f29a943acf1585e034d2f28cdba5r1-500-500v2_hq.jpg', 70),
	(258, 'https://newfs.s3.amazonaws.com/taxon-images-1000s1000/Asteraceae/achillea-millefolium-lanulosa-fl-gmittelhauser-c.jpg', 20),
	(259, 'https://static.positivr.fr/wp-content/uploads/2022/05/shutterstock_1747435874-768x512.jpg', 20),
	(264, 'https://img.freepik.com/fotos-premium/planta-menta-mentha-piperita_469558-16610.jpg', 2),
	(265, 'https://www.lasaponaria.es/img/cms/menta-immagine.jpg', 2),
	(266, 'https://previews.123rf.com/images/jobrestful/jobrestful1503/jobrestful150300018/37435788-mentha-cordifolia-or-or-mentha-piperita-peppermint-plant.jpg', 2),
	(267, 'https://www.geelfloricultura.com/media/2023/12/menta-piperita.png', 2),
	(268, 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Pfefferminze_natur_peppermint.jpg/330px-Pfefferminze_natur_peppermint.jpg', 2),
	(269, 'https://www.rivareno.com/wp-content/uploads/2019/06/Menta-piperita.jpg', 2),
	(270, 'https://www.shutterstock.com/image-illustration/drawing-mint-plant-flowers-green-260nw-2316032439.jpg', 2),
	(271, 'https://thumbs.dreamstime.com/b/flor-de-menta-vectorial-ejemplo-exhausto-dibujo-la-mano-del-piperita-mentha-flower-s-201860129.jpg', 2),
	(272, 'https://www.shutterstock.com/image-vector/vector-illustration-mentha-aquatica-watermint-260nw-2451256109.jpg', 2);

-- Volcando estructura para tabla bdplantas.nombres_comunes
CREATE TABLE IF NOT EXISTS `nombres_comunes` (
  `idNombrecomun` int(11) NOT NULL AUTO_INCREMENT,
  `nombreComun` varchar(40) NOT NULL,
  `fk_plantas` int(11) NOT NULL,
  PRIMARY KEY (`idNombrecomun`),
  KEY `fk_plantas` (`fk_plantas`),
  CONSTRAINT `nombres_comunes_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=274 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla bdplantas.nombres_comunes: ~100 rows (aproximadamente)
INSERT INTO `nombres_comunes` (`idNombrecomun`, `nombreComun`, `fk_plantas`) VALUES
	(1, 'Manzanilla', 1),
	(3, 'Rosa mosqueta', 3),
	(4, 'Papa nativa', 4),
	(5, 'Manayupa', 5),
	(6, 'Llantén', 6),
	(7, 'Malva', 7),
	(8, 'Hinojo', 8),
	(9, 'Hierba golondrina', 9),
	(10, 'Geranio andino', 10),
	(11, 'Chilca', 11),
	(12, 'Muña', 12),
	(13, 'Frambuesa andina', 13),
	(14, 'Rocoto', 14),
	(15, 'Tarwi', 15),
	(16, 'Camomila', 1),
	(18, 'Escaramujo', 3),
	(19, 'Patata andina', 4),
	(20, 'Pie de perro', 5),
	(31, 'Verbena', 22),
	(32, 'Verbena macho', 22),
	(33, 'Verbena mayor', 22),
	(34, 'Orégano pequeño', 23),
	(39, 'Clivia', 26),
	(40, 'Clivia Flores Naranja', 26),
	(41, 'Agapantus', 26),
	(42, 'Hojaslargas', 26),
	(43, 'Colio', 26),
	(50, 'Vejiga de perro', 29),
	(51, 'Chibombitas', 29),
	(52, 'Popita', 29),
	(53, 'Romero', 30),
	(54, 'Yerba de la niña', 30),
	(55, 'Roméro', 30),
	(61, 'Matico', 32),
	(62, 'Cordoncillo', 32),
	(63, 'Higuillo', 32),
	(64, 'Higuillo oloroso', 32),
	(65, 'Platanillo de Cuba', 32),
	(66, 'Dormilona', 44),
	(67, 'Mimosa', 44),
	(68, 'Sensitiva', 44),
	(141, 'Apazote', 31),
	(142, 'Apozote', 31),
	(143, 'Epazote', 31),
	(144, 'Paico', 31),
	(145, 'Pazote', 31),
	(146, 'Anís', 52),
	(147, 'Hinojo', 52),
	(148, 'Janež', 52),
	(149, 'Anis', 52),
	(150, 'Anís verde', 52),
	(151, 'Absintio', 24),
	(152, 'Ajenjo', 24),
	(153, 'Pravi pelin', 24),
	(154, 'Absenta', 24),
	(160, 'Chichicaste', 54),
	(161, 'Ortiga', 54),
	(162, 'Ortiga grande', 54),
	(163, 'Ortiga mayor', 54),
	(164, 'Velika kopriva', 54),
	(171, 'Eucalipto', 28),
	(172, 'Eucalipto rojo', 28),
	(173, 'Eucalipto-negro', 28),
	(185, 'Ruda', 55),
	(186, 'Ruda común', 55),
	(187, 'Ruda de monte', 55),
	(188, 'Ruda hortense', 55),
	(189, 'Ruda mayor', 55),
	(196, 'Cedrón', 21),
	(197, 'Hierba Luisa', 21),
	(198, 'Yerba Luisa', 21),
	(204, 'Rabo gato', 67),
	(205, 'Zacate de la fuente', 67),
	(206, 'Cola de plumas', 67),
	(207, 'Cola de zorro', 67),
	(208, 'Pasto de elefante', 67),
	(209, 'Peashooter', 68),
	(210, 'Lanzaguisantes', 68),
	(224, 'Nopalillo-mal ojo', 69),
	(225, 'Muerdago', 69),
	(226, 'Disciplinaria', 69),
	(227, 'Para de pollo', 69),
	(228, 'Hombre desnudo', 69),
	(234, 'Alcatraz', 27),
	(235, 'Cala', 27),
	(236, 'Cartucho', 27),
	(242, 'Cola de caballo', 48),
	(243, 'Cola de caballo del campo', 48),
	(244, 'Cola de rata', 48),
	(245, 'Equiseto menor', 48),
	(246, 'Njivska preslica', 48),
	(257, 'Espadaña', 70),
	(258, 'Anea', 70),
	(259, 'Totora', 70),
	(260, 'Tule espidilla', 70),
	(261, 'Piriope', 70),
	(266, 'Milenrama', 20),
	(267, 'Plumajillo', 20),
	(272, 'Hierbabuena', 2),
	(273, 'Menta', 2);

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

-- Volcando datos para la tabla bdplantas.personas: ~10 rows (aproximadamente)
INSERT INTO `personas` (`idPersona`, `DNI`, `nombres`, `apellido1`, `apellido2`, `telefono`, `direccion`) VALUES
	(1, '12345678', 'Carlos Manuel', 'Rodríguez', 'Vásquez', '943123456', 'Jr. San Martín 123, Huaraz'),
	(2, '23456789', 'María Elena', 'Morales', 'Castillo', '943234567', 'Av. Luzuriaga 456, Huaraz'),
	(3, '34567890', 'José Antonio', 'Huamán', 'Torres', '943345678', 'Jr. Bolívar 789, Carhuaz'),
	(4, '45678901', 'Ana Rosa', 'Mejía', 'Solís', '943456789', 'Av. Confraternidad 321, Yungay'),
	(5, '56789012', 'Pedro Luis', 'Albornoz', 'Ramírez', '943567890', 'Jr. Sucre 654, Caraz'),
	(6, '67890123', 'Carmen Julia', 'Flores', 'Mendoza', '943678901', 'Av. Raymondi 987, Huaraz'),
	(7, '78901234', 'Miguel Ángel', 'Cordero', 'Espinoza', '943789012', 'Jr. Gamarra 147, Recuay'),
	(8, '89012345', 'Rosa María', 'Sandoval', 'Guerrero', '943890123', 'Av. Centenario 258, Huari'),
	(9, '90123456', 'Francisco Javier', 'Herrera', 'Campos', '943901234', 'Jr. Tarapacá 369, Pomabamba'),
	(10, '01234567', 'Lucía Mercedes', 'Villarreal', 'Ponte', '943012345', 'Av. Los Olivos 741, Chimbote');

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

-- Volcando datos para la tabla bdplantas.plantas: ~32 rows (aproximadamente)
INSERT INTO `plantas` (`idPlanta`, `nombreCientifico`, `fk_familiasplantas`) VALUES
	(1, 'Matricaria chamomilla', 1),
	(2, 'Mentha piperita', 2),
	(3, 'Rosa rubiginosa', 3),
	(4, 'Solanum tuberosum', 4),
	(5, 'Desmodium molliculum', 5),
	(6, 'Plantago major', 6),
	(7, 'Malva sylvestris', 7),
	(8, 'Foeniculum vulgare', 8),
	(9, 'Euphorbia hirta', 9),
	(10, 'Geranium sessiliflorum', 10),
	(11, 'Baccharis latifolia', 1),
	(12, 'Clinopodium pulchellum', 2),
	(13, 'Rubus roseus', 3),
	(14, 'Capsicum pubescens', 4),
	(15, 'Lupinus mutabilis', 5),
	(20, 'Achillea millefolium', 1),
	(21, 'Aloysia citrodora', 11),
	(22, 'Verbena officinalis', 11),
	(23, 'Lippia origanoides', 11),
	(24, 'Artemisia absinthium', 1),
	(26, 'Clivia miniata', 13),
	(27, 'Zantedeschia aethiopica', 14),
	(28, 'Eucalyptus camaldulensis', 16),
	(29, 'Physalis minima', 4),
	(30, 'Rosmarinus officinalis', 2),
	(31, 'Dysphania ambrosioides', 17),
	(32, 'Piper aduncum', 19),
	(44, 'Mimosa pudica', 5),
	(48, 'Equisetum arvense', 21),
	(52, 'Pimpinella anisum', 8),
	(54, 'Urtica dioica', 23),
	(55, 'Ruta graveolens', 24),
	(67, 'Cenchrus setaceus', 25),
	(68, 'Legumus bigsplatus', 5),
	(69, 'Rhipsalis baccifera', 26),
	(70, 'Typha latifolia', 27);

-- Volcando estructura para tabla bdplantas.plantas_registros
CREATE TABLE IF NOT EXISTS `plantas_registros` (
  `fk_plantas` int(11) NOT NULL,
  `fk_empleados` int(11) NOT NULL,
  KEY `fk_plantas` (`fk_plantas`),
  KEY `fk_empleados` (`fk_empleados`),
  CONSTRAINT `planta_registro_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`),
  CONSTRAINT `planta_registro_ibfk_2` FOREIGN KEY (`fk_empleados`) REFERENCES `empleados` (`idEmpleado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla bdplantas.plantas_registros: ~33 rows (aproximadamente)
INSERT INTO `plantas_registros` (`fk_plantas`, `fk_empleados`) VALUES
	(1, 1),
	(2, 1),
	(3, 2),
	(4, 2),
	(5, 3),
	(6, 3),
	(7, 4),
	(8, 4),
	(9, 5),
	(10, 5),
	(11, 6),
	(12, 6),
	(13, 1),
	(14, 2),
	(15, 3),
	(20, 3),
	(21, 5),
	(22, 5),
	(23, 5),
	(24, 5),
	(26, 4),
	(27, 3),
	(28, 5),
	(29, 1),
	(30, 1),
	(31, 1),
	(32, 1),
	(44, 1),
	(48, 1),
	(52, 1),
	(24, 1),
	(54, 1),
	(28, 1),
	(55, 1),
	(21, 1),
	(27, 1),
	(67, 1),
	(68, 1),
	(20, 1),
	(69, 1),
	(20, 2),
	(70, 1);

-- Volcando estructura para tabla bdplantas.provincias
CREATE TABLE IF NOT EXISTS `provincias` (
  `idprovincias` int(11) NOT NULL AUTO_INCREMENT,
  `nombreProvincia` varchar(45) NOT NULL,
  `fk_regiones` int(11) NOT NULL,
  PRIMARY KEY (`idprovincias`),
  KEY `fk_provincias_regiones1_idx` (`fk_regiones`),
  CONSTRAINT `fk_provincias_regiones1` FOREIGN KEY (`fk_regiones`) REFERENCES `regiones` (`idRegion`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla bdplantas.provincias: ~20 rows (aproximadamente)
INSERT INTO `provincias` (`idprovincias`, `nombreProvincia`, `fk_regiones`) VALUES
	(1, 'Huaraz', 1),
	(2, 'Aija', 1),
	(3, 'Antonio Raymondi', 1),
	(4, 'Asunción', 1),
	(5, 'Bolognesi', 1),
	(6, 'Carhuaz', 1),
	(7, 'Carlos Fermín Fitzcarrald', 1),
	(8, 'Casma', 1),
	(9, 'Corongo', 1),
	(10, 'Huari', 1),
	(11, 'Huarmey', 1),
	(12, 'Huaylas', 1),
	(13, 'Mariscal Luzuriaga', 1),
	(14, 'Ocros', 1),
	(15, 'Pallasca', 1),
	(16, 'Pomabamba', 1),
	(17, 'Recuay', 1),
	(18, 'Santa', 1),
	(19, 'Sihuas', 1),
	(20, 'Yungay', 1);

-- Volcando estructura para tabla bdplantas.provincia_ecoregion
CREATE TABLE IF NOT EXISTS `provincia_ecoregion` (
  `fk_ecoregiones` int(11) NOT NULL,
  `fk_provincias` int(11) NOT NULL,
  KEY `fk_provincia_ecoregion_ecoregiones1_idx` (`fk_ecoregiones`),
  KEY `fk_provincia_ecoregion_provincias1_idx` (`fk_provincias`),
  CONSTRAINT `fk_provincia_ecoregion_ecoregiones1` FOREIGN KEY (`fk_ecoregiones`) REFERENCES `ecoregiones` (`idecoregion`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_provincia_ecoregion_provincias1` FOREIGN KEY (`fk_provincias`) REFERENCES `provincias` (`idprovincias`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla bdplantas.provincia_ecoregion: ~33 rows (aproximadamente)
INSERT INTO `provincia_ecoregion` (`fk_ecoregiones`, `fk_provincias`) VALUES
	(1, 8),
	(1, 11),
	(1, 18),
	(3, 8),
	(3, 11),
	(3, 18),
	(6, 1),
	(6, 2),
	(6, 5),
	(6, 6),
	(6, 9),
	(6, 10),
	(6, 12),
	(6, 13),
	(6, 14),
	(6, 15),
	(6, 17),
	(6, 19),
	(6, 20),
	(7, 1),
	(7, 3),
	(7, 4),
	(7, 6),
	(7, 10),
	(7, 12),
	(7, 16),
	(7, 17),
	(7, 20),
	(9, 3),
	(9, 4),
	(9, 7),
	(9, 13),
	(9, 16);

-- Volcando estructura para tabla bdplantas.regiones
CREATE TABLE IF NOT EXISTS `regiones` (
  `idRegion` int(11) NOT NULL AUTO_INCREMENT,
  `region` varchar(50) NOT NULL,
  PRIMARY KEY (`idRegion`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla bdplantas.regiones: ~0 rows (aproximadamente)
INSERT INTO `regiones` (`idRegion`, `region`) VALUES
	(1, 'Ancash');

-- Volcando estructura para tabla bdplantas.saberes_culturales
CREATE TABLE IF NOT EXISTS `saberes_culturales` (
  `idSaberes` int(11) NOT NULL AUTO_INCREMENT,
  `descripcionSaber` text NOT NULL,
  `fk_plantas` int(11) NOT NULL,
  PRIMARY KEY (`idSaberes`),
  KEY `fk_plantas` (`fk_plantas`),
  CONSTRAINT `saberesculturales_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla bdplantas.saberes_culturales: ~10 rows (aproximadamente)
INSERT INTO `saberes_culturales` (`idSaberes`, `descripcionSaber`, `fk_plantas`) VALUES
	(1, 'Los curanderos de Ancash utilizan la manzanilla para limpias espirituales y calmar el susto en niños', 1),
	(2, 'La menta es usada en ceremonias de sanación para purificar el ambiente', 2),
	(3, 'La rosa mosqueta se recolecta en luna llena para potenciar sus propiedades curativas', 3),
	(4, 'Las papas nativas son consideradas sagradas y se usan en rituales de abundancia', 4),
	(5, 'La manayupa es conocida como la planta de los riñones en la medicina tradicional ancashina', 5),
	(6, 'El llantén es llamado siete venas y se usa para curar heridas de animales', 6),
	(7, 'La malva se utiliza en baños rituales para la buena suerte', 7),
	(8, 'El hinojo se quema como sahumerio para alejar malas energías', 8),
	(9, 'La hierba golondrina se usa para quitar verrugas según la tradición local', 9),
	(10, 'El geranio andino se planta cerca de las casas para protección', 10),
	(11, 'Tradicionalmente, se utiliza para tratar diversas dolencias, incluyendo problemas respiratorios, hepáticos y como antiinflamatorio', 5);

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

-- Volcando datos para la tabla bdplantas.tipos_aportes: ~8 rows (aproximadamente)
INSERT INTO `tipos_aportes` (`idTipoAporte`, `nombreTipo`) VALUES
	(1, 'Propiedades medicinales'),
	(2, 'Métodos de preparación'),
	(3, 'Ubicación geográfica'),
	(4, 'Época de recolección'),
	(5, 'Contraindicaciones'),
	(6, 'Usos tradicionales'),
	(7, 'Características morfológicas'),
	(8, 'Cultivo y propagación');

-- Volcando estructura para tabla bdplantas.ubicaciones_nombres
CREATE TABLE IF NOT EXISTS `ubicaciones_nombres` (
  `fk_nombres_comunes` int(11) NOT NULL,
  `fk_regiones` int(11) NOT NULL,
  KEY `fk_nombres_comunes1_idx` (`fk_nombres_comunes`),
  KEY `fk_ubicaciones_nombres_regiones1_idx` (`fk_regiones`),
  CONSTRAINT `fk_nombres_comunes1` FOREIGN KEY (`fk_nombres_comunes`) REFERENCES `nombres_comunes` (`idNombrecomun`),
  CONSTRAINT `fk_ubicaciones_nombres_regiones1` FOREIGN KEY (`fk_regiones`) REFERENCES `regiones` (`idRegion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Volcando datos para la tabla bdplantas.ubicaciones_nombres: ~0 rows (aproximadamente)

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

-- Volcando datos para la tabla bdplantas.usos: ~16 rows (aproximadamente)
INSERT INTO `usos` (`idUsos`, `parte`, `uso`, `contraIndicaciones`, `preparacion`, `fk_plantas`) VALUES
	(1, 'Flores', 'Digestivo', 'Embarazo', 'Infusión', 1),
	(2, 'Hojas', 'Digestivo', 'Ninguna conocida', 'Té', 2),
	(3, 'Frutos', 'Vitamina C', 'Ninguna conocida', 'Mermelada', 3),
	(4, 'Tubérculos', 'Antiinflamatorio', 'Diabetes', 'Cataplasma', 4),
	(5, 'Hojas', 'Riñones', 'Embarazo', 'Cocimiento', 5),
	(6, 'Hojas', 'Heridas', 'Ninguna conocida', 'Cataplasma', 6),
	(7, 'Flores', 'Tos', 'Ninguna conocida', 'Jarabe', 7),
	(8, 'Semillas', 'Digestivo', 'Embarazo', 'Infusión', 8),
	(9, 'Hojas', 'Heridas', 'Piel sensible', 'Aplicación directa', 9),
	(10, 'Hojas', 'Diarrea', 'Ninguna conocida', 'Infusión', 10),
	(11, 'Hojas', 'Resfríos', 'Hipertensión', 'Vaporizaciones', 11),
	(12, 'Hojas', 'Digestivo', 'Ninguna conocida', 'Condimento', 12),
	(13, 'Frutos', 'Antioxidante', 'Ninguna conocida', 'Consumo directo', 13),
	(14, 'Frutos', 'Vitamina C', 'Gastritis', 'Salsa', 14),
	(15, 'Semillas', 'Proteínas', 'Favismo', 'Cocido', 15);

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

-- Volcando datos para la tabla bdplantas.usuarios: ~6 rows (aproximadamente)
INSERT INTO `usuarios` (`idUsuario`, `usuario`, `contraseña`, `fk_empleados`) VALUES
	(1, 'crodriguez', 'aafdc23870ecbcd3d557b6423a8982134e17927e', 1),
	(2, 'mmorales', 'ff37a98a9963d347e9749a5c1b3936a4a245a6ff', 2),
	(3, 'jhuaman', 'f6e81a2e41ae36dca6fc0aafc1126a787bd8cd60', 3),
	(4, 'amejia', 'a75b9cb109043793526d3d3bcb55102ea0431532', 4),
	(5, 'palbornoz', '35892de37b002a82031167829d4a74f05e1f4cd3', 5),
	(6, 'cflores', 'a5f6b0826338300b814df557d460a1598026d174', 6);

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
