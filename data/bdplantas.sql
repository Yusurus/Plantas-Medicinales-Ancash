-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: bdplantasv3
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `aportes_expertos`
--

DROP TABLE IF EXISTS `aportes_expertos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aportes_expertos` (
  `idAporteExperto` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `descripcion` text NOT NULL,
  `fk_personas` int NOT NULL,
  `fk_plantas` int NOT NULL,
  `fk_tipos_aportes` int NOT NULL,
  PRIMARY KEY (`idAporteExperto`),
  KEY `fk_persona` (`fk_personas`),
  KEY `fk_planta` (`fk_plantas`),
  KEY `fk_tipoAporte` (`fk_tipos_aportes`),
  CONSTRAINT `aporte_experto_ibfk_1` FOREIGN KEY (`fk_personas`) REFERENCES `personas` (`idPersona`),
  CONSTRAINT `aporte_experto_ibfk_2` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`),
  CONSTRAINT `aporte_experto_ibfk_3` FOREIGN KEY (`fk_tipos_aportes`) REFERENCES `tipos_aportes` (`idTipoAporte`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aportes_expertos`
--

LOCK TABLES `aportes_expertos` WRITE;
/*!40000 ALTER TABLE `aportes_expertos` DISABLE KEYS */;
INSERT INTO `aportes_expertos` VALUES (1,'2024-01-15','La manzanilla de Ancash tiene mayor concentración de aceites esenciales que otras variedades',7,1,1),(2,'2024-01-20','Se recomienda recolectar las flores en las primeras horas de la mañana',8,1,4),(3,'2024-02-10','La menta crece mejor en las quebradas húmedas de la Cordillera Blanca',9,2,3),(4,'2024-02-15','Método tradicional de secado en sombra para conservar propiedades',10,2,2),(5,'2024-03-05','Rosa mosqueta abundante en altitudes entre 3000-3800 msnm en Ancash',7,3,3),(6,'2024-03-12','Las papas nativas tienen propiedades antiinflamatorias únicas',8,4,1),(7,'2024-04-01','Manayupa efectiva para problemas renales según estudios locales',9,5,1),(8,'2024-04-08','Llantén muy común en caminos de herradura de toda la región',10,6,3),(9,'2024-05-03','Malva útil para problemas respiratorios en clima frío de altura',7,7,1),(10,'2024-05-10','Hinojo cultivado tradicionalmente en huertos familiares ancashinos',8,8,8);
/*!40000 ALTER TABLE `aportes_expertos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `archivaciones_saberes`
--

DROP TABLE IF EXISTS `archivaciones_saberes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `archivaciones_saberes` (
  `idArchivaSaber` int NOT NULL AUTO_INCREMENT,
  `fechaArchivaSaber` date NOT NULL,
  `motivoArchivaSaber` text NOT NULL,
  `fk_saberes_culturales` int NOT NULL,
  `fk_empleados` int NOT NULL,
  PRIMARY KEY (`idArchivaSaber`),
  KEY `fk_saberes` (`fk_saberes_culturales`),
  KEY `empleado_idEmpleado` (`fk_empleados`),
  CONSTRAINT `archivacionessaberes_ibfk_1` FOREIGN KEY (`fk_saberes_culturales`) REFERENCES `saberes_culturales` (`idSaberes`),
  CONSTRAINT `archivacionessaberes_ibfk_2` FOREIGN KEY (`fk_empleados`) REFERENCES `empleados` (`idEmpleado`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `archivaciones_saberes`
--

LOCK TABLES `archivaciones_saberes` WRITE;
/*!40000 ALTER TABLE `archivaciones_saberes` DISABLE KEYS */;
INSERT INTO `archivaciones_saberes` VALUES (1,'2024-07-01','Información no verificada por comunidad local',1,3),(2,'2024-07-10','Práctica ya no utilizada en la región',5,4);
/*!40000 ALTER TABLE `archivaciones_saberes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `archivaciones_ubicaciones`
--

DROP TABLE IF EXISTS `archivaciones_ubicaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `archivaciones_ubicaciones` (
  `idArchivaUbi` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `motivo` text NOT NULL,
  `fk_idubicaciones` int NOT NULL,
  `fk_idempleados` int NOT NULL,
  PRIMARY KEY (`idArchivaUbi`),
  KEY `fk_ubicaciones` (`fk_idubicaciones`),
  KEY `empleado_idEmpleado` (`fk_idempleados`),
  CONSTRAINT `archivacionesubicaciones_ibfk_1` FOREIGN KEY (`fk_idubicaciones`) REFERENCES `regiones` (`idRegion`),
  CONSTRAINT `archivacionesubicaciones_ibfk_2` FOREIGN KEY (`fk_idempleados`) REFERENCES `empleados` (`idEmpleado`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `archivaciones_ubicaciones`
--

LOCK TABLES `archivaciones_ubicaciones` WRITE;
/*!40000 ALTER TABLE `archivaciones_ubicaciones` DISABLE KEYS */;
INSERT INTO `archivaciones_ubicaciones` VALUES (1,'2024-08-01','Cambio en clasificación de ecoregiones',1,5),(2,'2024-08-15','Actualización de límites regionales',1,6);
/*!40000 ALTER TABLE `archivaciones_ubicaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `archivaciones_usos`
--

DROP TABLE IF EXISTS `archivaciones_usos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `archivaciones_usos` (
  `idArchivaUso` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `motivo` text NOT NULL,
  `fk_usos` int NOT NULL,
  `fk_empleados` int NOT NULL,
  PRIMARY KEY (`idArchivaUso`),
  KEY `fk_archivaciones_usos_usos1_idx` (`fk_usos`),
  KEY `fk_archivaciones_usos_empleados1_idx` (`fk_empleados`),
  CONSTRAINT `fk_archivaciones_usos_empleados1` FOREIGN KEY (`fk_empleados`) REFERENCES `empleados` (`idEmpleado`),
  CONSTRAINT `fk_archivaciones_usos_usos1` FOREIGN KEY (`fk_usos`) REFERENCES `usos` (`idUsos`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `archivaciones_usos`
--

LOCK TABLES `archivaciones_usos` WRITE;
/*!40000 ALTER TABLE `archivaciones_usos` DISABLE KEYS */;
INSERT INTO `archivaciones_usos` VALUES (1,'2024-09-01','Contraindicación no confirmada científicamente',1,1),(2,'2024-09-10','Método de preparación actualizado',8,2);
/*!40000 ALTER TABLE `archivaciones_usos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `archivacionesplantas`
--

DROP TABLE IF EXISTS `archivacionesplantas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `archivacionesplantas` (
  `idArchivaPlanta` int NOT NULL AUTO_INCREMENT,
  `fecha` date NOT NULL,
  `motivo` text NOT NULL,
  `fk_plantas` int NOT NULL,
  `fk_empleados` int NOT NULL,
  PRIMARY KEY (`idArchivaPlanta`),
  KEY `fk_plantas` (`fk_plantas`),
  KEY `empleado_idEmpleado` (`fk_empleados`),
  CONSTRAINT `archivacionesplanta_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`),
  CONSTRAINT `archivacionesplanta_ibfk_2` FOREIGN KEY (`fk_empleados`) REFERENCES `empleados` (`idEmpleado`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `archivacionesplantas`
--

LOCK TABLES `archivacionesplantas` WRITE;
/*!40000 ALTER TABLE `archivacionesplantas` DISABLE KEYS */;
INSERT INTO `archivacionesplantas` VALUES (1,'2024-06-01','Planta ya no encontrada en ubicación original registrada',1,1),(2,'2024-06-15','Información duplicada con otro registro',11,2);
/*!40000 ALTER TABLE `archivacionesplantas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cargos`
--

DROP TABLE IF EXISTS `cargos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cargos` (
  `idCargo` int NOT NULL AUTO_INCREMENT,
  `categoria` varchar(50) NOT NULL,
  `salario` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idCargo`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargos`
--

LOCK TABLES `cargos` WRITE;
/*!40000 ALTER TABLE `cargos` DISABLE KEYS */;
INSERT INTO `cargos` VALUES (1,'Botánico Senior',3500.00),(2,'Etnobotánico',3200.00),(3,'Investigador Junior',2800.00),(4,'Curador de Herbario',3000.00),(5,'Técnico de Campo',2500.00),(6,'Administrador BD',3300.00);
/*!40000 ALTER TABLE `cargos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `datos_morfologicos`
--

DROP TABLE IF EXISTS `datos_morfologicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `datos_morfologicos` (
  `idDatomorfologico` int NOT NULL AUTO_INCREMENT,
  `datoMorfologico` int NOT NULL,
  `fk_plantas` int NOT NULL,
  PRIMARY KEY (`idDatomorfologico`),
  KEY `fk_plantas` (`fk_plantas`),
  CONSTRAINT `datosmorfologicos_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datos_morfologicos`
--

LOCK TABLES `datos_morfologicos` WRITE;
/*!40000 ALTER TABLE `datos_morfologicos` DISABLE KEYS */;
INSERT INTO `datos_morfologicos` VALUES (1,1,1),(2,2,2),(3,3,3),(4,4,4),(5,5,5),(6,6,6),(7,7,7),(8,8,8),(9,9,9),(10,10,10),(11,11,11),(12,12,12),(13,13,13),(14,14,14),(15,15,15);
/*!40000 ALTER TABLE `datos_morfologicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ecoregiones`
--

DROP TABLE IF EXISTS `ecoregiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ecoregiones` (
  `idecoregion` int NOT NULL AUTO_INCREMENT,
  `ecoregion` varchar(45) NOT NULL,
  `fk_plantas` int NOT NULL,
  PRIMARY KEY (`idecoregion`),
  KEY `fk_ecoregiones_plantas1_idx` (`fk_plantas`),
  CONSTRAINT `fk_ecoregiones_plantas1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ecoregiones`
--

LOCK TABLES `ecoregiones` WRITE;
/*!40000 ALTER TABLE `ecoregiones` DISABLE KEYS */;
INSERT INTO `ecoregiones` VALUES (1,'Desierto del Pacífico',1),(2,'Serranía Esteparia',2),(3,'Serranía Esteparia',3),(4,'Serranía Esteparia',4),(5,'Jalca',5),(6,'Jalca',6),(7,'Puna',7),(8,'Puna',8),(9,'Desierto del Pacífico',9),(10,'Serranía Esteparia',10),(11,'Jalca',11),(12,'Puna',12),(13,'Serranía Esteparia',13),(14,'Serranía Esteparia',14),(15,'Serranía Esteparia',15);
/*!40000 ALTER TABLE `ecoregiones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleados`
--

DROP TABLE IF EXISTS `empleados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleados` (
  `idEmpleado` int NOT NULL AUTO_INCREMENT,
  `correo` varchar(50) NOT NULL,
  `fk_personas` int NOT NULL,
  `fk_cargos` int NOT NULL,
  PRIMARY KEY (`idEmpleado`),
  KEY `fk_personas` (`fk_personas`),
  KEY `fk_cargos` (`fk_cargos`),
  CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`fk_personas`) REFERENCES `personas` (`idPersona`),
  CONSTRAINT `empleado_ibfk_2` FOREIGN KEY (`fk_cargos`) REFERENCES `cargos` (`idCargo`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleados`
--

LOCK TABLES `empleados` WRITE;
/*!40000 ALTER TABLE `empleados` DISABLE KEYS */;
INSERT INTO `empleados` VALUES (1,'carlos.rodriguez@plantasancash.pe',1,1),(2,'maria.morales@plantasancash.pe',2,2),(3,'jose.huaman@plantasancash.pe',3,3),(4,'ana.mejia@plantasancash.pe',4,4),(5,'pedro.albornoz@plantasancash.pe',5,5),(6,'carmen.flores@plantasancash.pe',6,6);
/*!40000 ALTER TABLE `empleados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `familias_plantas`
--

DROP TABLE IF EXISTS `familias_plantas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `familias_plantas` (
  `idfamiliaPlanta` int NOT NULL AUTO_INCREMENT,
  `nomFamilia` varchar(45) NOT NULL,
  PRIMARY KEY (`idfamiliaPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `familias_plantas`
--

LOCK TABLES `familias_plantas` WRITE;
/*!40000 ALTER TABLE `familias_plantas` DISABLE KEYS */;
INSERT INTO `familias_plantas` VALUES (1,'Asteraceae'),(2,'Lamiaceae'),(3,'Rosaceae'),(4,'Solanaceae'),(5,'Fabaceae'),(6,'Plantaginaceae'),(7,'Malvaceae'),(8,'Apiaceae'),(9,'Euphorbiaceae'),(10,'Geraniaceae');
/*!40000 ALTER TABLE `familias_plantas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `linksimagenes`
--

DROP TABLE IF EXISTS `linksimagenes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `linksimagenes` (
  `idLinksImagenes` int NOT NULL AUTO_INCREMENT,
  `linkImagen` mediumtext NOT NULL,
  `fk_plantas` int NOT NULL,
  PRIMARY KEY (`idLinksImagenes`),
  KEY `fk_linksImagenes_plantas1_idx` (`fk_plantas`),
  CONSTRAINT `fk_linksImagenes_plantas1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `linksimagenes`
--

LOCK TABLES `linksimagenes` WRITE;
/*!40000 ALTER TABLE `linksimagenes` DISABLE KEYS */;
INSERT INTO `linksimagenes` VALUES (1,'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcTuzSCCbhGuXz0ho2AtwXon5XTOw1CDkdhzYkhERxcMae1pV5k1CcixvUShCVtSulmHxGUygE8kqENtfYBXYku0qQ',1),(2,'https://www.lasaponaria.es/img/cms/menta-immagine.jpg',2),(3,'https://www.trevorwhiteroses.co.uk/wp-content/uploads/2018/02/Rosa-rubiginosa-amy-robstart-species-rose.jpg',3),(4,'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/S._tuberosum-5.JPG/500px-S._tuberosum-5.JPG',4),(5,'https://www.algemica.com/web/image/8965/desmodium-2.jpg?access_token=10ce110c-fdd2-4e23-99d0-34d24e4b4b7f',5),(6,'https://m.media-amazon.com/images/I/61rSPQMt9EL._AC_UF894,1000_QL80_.jpg',6),(7,'https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Mallow_January_2008-1.jpg/1200px-Mallow_January_2008-1.jpg',7),(8,'https://plantasflores.com/wp-content/uploads/2024/09/Foeniculum-vulgare.webp',8),(9,'https://portal.wiktrop.org/files-api/api/get/crop/img//Euphorbia%20hirta/ephhi_20120201_151612.jpg?h=500',9),(10,'https://www.chileflora.com/Florachilena/ImagesHigh/IMG_3648.jpg',10),(11,'https://cloudfront-us-east-1.images.arcpublishing.com/infobae/UGKMUTXRGZDYZMVYWZBBLD4LK4.png',11),(12,'https://inaturalist-open-data.s3.amazonaws.com/photos/261661343/large.jpeg',12),(13,'https://upload.wikimedia.org/wikipedia/commons/5/50/Rubus_Roseus_-_Flickr_-_Dick_Culbert.jpg',13),(14,'https://fm-digital-assets.fieldmuseum.org/1511/600/SOLA_caps_pube_per_22552.jpg',14),(15,'https://upload.wikimedia.org/wikipedia/commons/8/83/Peruvian_Field_Lupines.jpg',15),(16,'https://img.freepik.com/fotos-premium/planta-menta-mentha-piperita_469558-16610.jpg',2);
/*!40000 ALTER TABLE `linksimagenes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nombres_comunes`
--

DROP TABLE IF EXISTS `nombres_comunes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nombres_comunes` (
  `idNombrecomun` int NOT NULL AUTO_INCREMENT,
  `nombreComun` varchar(20) NOT NULL,
  `fk_plantas` int NOT NULL,
  PRIMARY KEY (`idNombrecomun`),
  KEY `fk_plantas` (`fk_plantas`),
  CONSTRAINT `nombres_comunes_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nombres_comunes`
--

LOCK TABLES `nombres_comunes` WRITE;
/*!40000 ALTER TABLE `nombres_comunes` DISABLE KEYS */;
INSERT INTO `nombres_comunes` VALUES (1,'Manzanilla',1),(2,'Menta',2),(3,'Rosa mosqueta',3),(4,'Papa nativa',4),(5,'Manayupa',5),(6,'Llantén',6),(7,'Malva',7),(8,'Hinojo',8),(9,'Hierba golondrina',9),(10,'Geranio andino',10),(11,'Chilca',11),(12,'Muña',12),(13,'Frambuesa andina',13),(14,'Rocoto',14),(15,'Tarwi',15),(16,'Camomila',1),(17,'Hierbabuena',2),(18,'Escaramujo',3),(19,'Patata andina',4),(20,'Pie de perro',5);
/*!40000 ALTER TABLE `nombres_comunes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personas`
--

DROP TABLE IF EXISTS `personas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personas` (
  `idPersona` int NOT NULL AUTO_INCREMENT,
  `DNI` varchar(8) NOT NULL,
  `nombres` varchar(50) NOT NULL,
  `apellido1` varchar(45) NOT NULL,
  `apellido2` varchar(45) NOT NULL,
  `telefono` varchar(9) NOT NULL,
  `direccion` varchar(100) NOT NULL,
  PRIMARY KEY (`idPersona`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personas`
--

LOCK TABLES `personas` WRITE;
/*!40000 ALTER TABLE `personas` DISABLE KEYS */;
INSERT INTO `personas` VALUES (1,'12345678','Carlos Manuel','Rodríguez','Vásquez','943123456','Jr. San Martín 123, Huaraz'),(2,'23456789','María Elena','Morales','Castillo','943234567','Av. Luzuriaga 456, Huaraz'),(3,'34567890','José Antonio','Huamán','Torres','943345678','Jr. Bolívar 789, Carhuaz'),(4,'45678901','Ana Rosa','Mejía','Solís','943456789','Av. Confraternidad 321, Yungay'),(5,'56789012','Pedro Luis','Albornoz','Ramírez','943567890','Jr. Sucre 654, Caraz'),(6,'67890123','Carmen Julia','Flores','Mendoza','943678901','Av. Raymondi 987, Huaraz'),(7,'78901234','Miguel Ángel','Cordero','Espinoza','943789012','Jr. Gamarra 147, Recuay'),(8,'89012345','Rosa María','Sandoval','Guerrero','943890123','Av. Centenario 258, Huari'),(9,'90123456','Francisco Javier','Herrera','Campos','943901234','Jr. Tarapacá 369, Pomabamba'),(10,'01234567','Lucía Mercedes','Villarreal','Ponte','943012345','Av. Los Olivos 741, Chimbote');
/*!40000 ALTER TABLE `personas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plantas`
--

DROP TABLE IF EXISTS `plantas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plantas` (
  `idPlanta` int NOT NULL AUTO_INCREMENT,
  `nombreCientifico` varchar(50) NOT NULL,
  `fk_familiasplantas` int NOT NULL,
  PRIMARY KEY (`idPlanta`),
  KEY `familiasPlantas_idfamiliasPlantas` (`fk_familiasplantas`),
  CONSTRAINT `plantas_ibfk_1` FOREIGN KEY (`fk_familiasplantas`) REFERENCES `familias_plantas` (`idfamiliaPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plantas`
--

LOCK TABLES `plantas` WRITE;
/*!40000 ALTER TABLE `plantas` DISABLE KEYS */;
INSERT INTO `plantas` VALUES (1,'Matricaria chamomilla',1),(2,'Mentha piperita',2),(3,'Rosa rubiginosa',3),(4,'Solanum tuberosum',4),(5,'Desmodium molliculum',5),(6,'Plantago major',6),(7,'Malva sylvestris',7),(8,'Foeniculum vulgare',8),(9,'Euphorbia hirta',9),(10,'Geranium sessiliflorum',10),(11,'Baccharis latifolia',1),(12,'Clinopodium pulchellum',2),(13,'Rubus roseus',3),(14,'Capsicum pubescens',4),(15,'Lupinus mutabilis',5);
/*!40000 ALTER TABLE `plantas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plantas_registros`
--

DROP TABLE IF EXISTS `plantas_registros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plantas_registros` (
  `fk_plantas` int NOT NULL,
  `fk_empleados` int NOT NULL,
  KEY `fk_plantas` (`fk_plantas`),
  KEY `fk_empleados` (`fk_empleados`),
  CONSTRAINT `planta_registro_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`),
  CONSTRAINT `planta_registro_ibfk_2` FOREIGN KEY (`fk_empleados`) REFERENCES `empleados` (`idEmpleado`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plantas_registros`
--

LOCK TABLES `plantas_registros` WRITE;
/*!40000 ALTER TABLE `plantas_registros` DISABLE KEYS */;
INSERT INTO `plantas_registros` VALUES (1,1),(2,1),(3,2),(4,2),(5,3),(6,3),(7,4),(8,4),(9,5),(10,5),(11,6),(12,6),(13,1),(14,2),(15,3);
/*!40000 ALTER TABLE `plantas_registros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region_ecoregion`
--

DROP TABLE IF EXISTS `region_ecoregion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `region_ecoregion` (
  `fk_ecoregiones` int NOT NULL,
  `fk_regiones` int NOT NULL,
  KEY `fk_region_ecoregion_ecoregiones1_idx` (`fk_ecoregiones`),
  KEY `fk_region_ecoregion_regiones1_idx` (`fk_regiones`),
  CONSTRAINT `fk_region_ecoregion_ecoregiones1` FOREIGN KEY (`fk_ecoregiones`) REFERENCES `ecoregiones` (`idecoregion`),
  CONSTRAINT `fk_region_ecoregion_regiones1` FOREIGN KEY (`fk_regiones`) REFERENCES `regiones` (`idRegion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region_ecoregion`
--

LOCK TABLES `region_ecoregion` WRITE;
/*!40000 ALTER TABLE `region_ecoregion` DISABLE KEYS */;
INSERT INTO `region_ecoregion` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1);
/*!40000 ALTER TABLE `region_ecoregion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `regiones`
--

DROP TABLE IF EXISTS `regiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `regiones` (
  `idRegion` int NOT NULL AUTO_INCREMENT,
  `region` varchar(50) NOT NULL,
  PRIMARY KEY (`idRegion`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regiones`
--

LOCK TABLES `regiones` WRITE;
/*!40000 ALTER TABLE `regiones` DISABLE KEYS */;
INSERT INTO `regiones` VALUES (1,'Ancash');
/*!40000 ALTER TABLE `regiones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `saberes_culturales`
--

DROP TABLE IF EXISTS `saberes_culturales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `saberes_culturales` (
  `idSaberes` int NOT NULL AUTO_INCREMENT,
  `descripcionSaber` text NOT NULL,
  `fk_plantas` int NOT NULL,
  PRIMARY KEY (`idSaberes`),
  KEY `fk_plantas` (`fk_plantas`),
  CONSTRAINT `saberesculturales_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `saberes_culturales`
--

LOCK TABLES `saberes_culturales` WRITE;
/*!40000 ALTER TABLE `saberes_culturales` DISABLE KEYS */;
INSERT INTO `saberes_culturales` VALUES (1,'Los curanderos de Ancash utilizan la manzanilla para limpias espirituales y calmar el susto en niños',1),(2,'La menta es usada en ceremonias de sanación para purificar el ambiente',2),(3,'La rosa mosqueta se recolecta en luna llena para potenciar sus propiedades curativas',3),(4,'Las papas nativas son consideradas sagradas y se usan en rituales de abundancia',4),(5,'La manayupa es conocida como la planta de los riñones en la medicina tradicional ancashina',5),(6,'El llantén es llamado siete venas y se usa para curar heridas de animales',6),(7,'La malva se utiliza en baños rituales para la buena suerte',7),(8,'El hinojo se quema como sahumerio para alejar malas energías',8),(9,'La hierba golondrina se usa para quitar verrugas según la tradición local',9),(10,'El geranio andino se planta cerca de las casas para protección',10);
/*!40000 ALTER TABLE `saberes_culturales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipos_aportes`
--

DROP TABLE IF EXISTS `tipos_aportes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipos_aportes` (
  `idTipoAporte` int NOT NULL AUTO_INCREMENT,
  `nombreTipo` varchar(100) NOT NULL,
  PRIMARY KEY (`idTipoAporte`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipos_aportes`
--

LOCK TABLES `tipos_aportes` WRITE;
/*!40000 ALTER TABLE `tipos_aportes` DISABLE KEYS */;
INSERT INTO `tipos_aportes` VALUES (1,'Propiedades medicinales'),(2,'Métodos de preparación'),(3,'Ubicación geográfica'),(4,'Época de recolección'),(5,'Contraindicaciones'),(6,'Usos tradicionales'),(7,'Características morfológicas'),(8,'Cultivo y propagación');
/*!40000 ALTER TABLE `tipos_aportes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ubicaciones_nombres`
--

DROP TABLE IF EXISTS `ubicaciones_nombres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ubicaciones_nombres` (
  `fk_nombres_comunes` int NOT NULL,
  `fk_regiones` int NOT NULL,
  KEY `fk_nombres_comunes1_idx` (`fk_nombres_comunes`),
  KEY `fk_ubicaciones_nombres_regiones1_idx` (`fk_regiones`),
  CONSTRAINT `fk_nombres_comunes1` FOREIGN KEY (`fk_nombres_comunes`) REFERENCES `nombres_comunes` (`idNombrecomun`),
  CONSTRAINT `fk_ubicaciones_nombres_regiones1` FOREIGN KEY (`fk_regiones`) REFERENCES `regiones` (`idRegion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ubicaciones_nombres`
--

LOCK TABLES `ubicaciones_nombres` WRITE;
/*!40000 ALTER TABLE `ubicaciones_nombres` DISABLE KEYS */;
INSERT INTO `ubicaciones_nombres` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(19,1),(20,1);
/*!40000 ALTER TABLE `ubicaciones_nombres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usos`
--

DROP TABLE IF EXISTS `usos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usos` (
  `idUsos` int NOT NULL AUTO_INCREMENT,
  `parte` varchar(50) NOT NULL,
  `uso` varchar(50) NOT NULL,
  `contraIndicaciones` varchar(80) NOT NULL,
  `preparacion` varchar(80) NOT NULL,
  `fk_plantas` int NOT NULL,
  PRIMARY KEY (`idUsos`),
  KEY `fk_plantas` (`fk_plantas`),
  CONSTRAINT `usos_ibfk_1` FOREIGN KEY (`fk_plantas`) REFERENCES `plantas` (`idPlanta`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usos`
--

LOCK TABLES `usos` WRITE;
/*!40000 ALTER TABLE `usos` DISABLE KEYS */;
INSERT INTO `usos` VALUES (1,'Flores','Digestivo','Embarazo','Infusión',1),(2,'Hojas','Digestivo','Ninguna conocida','Té',2),(3,'Frutos','Vitamina C','Ninguna conocida','Mermelada',3),(4,'Tubérculos','Antiinflamatorio','Diabetes','Cataplasma',4),(5,'Hojas','Riñones','Embarazo','Cocimiento',5),(6,'Hojas','Heridas','Ninguna conocida','Cataplasma',6),(7,'Flores','Tos','Ninguna conocida','Jarabe',7),(8,'Semillas','Digestivo','Embarazo','Infusión',8),(9,'Hojas','Heridas','Piel sensible','Aplicación directa',9),(10,'Hojas','Diarrea','Ninguna conocida','Infusión',10),(11,'Hojas','Resfríos','Hipertensión','Vaporizaciones',11),(12,'Hojas','Digestivo','Ninguna conocida','Condimento',12),(13,'Frutos','Antioxidante','Ninguna conocida','Consumo directo',13),(14,'Frutos','Vitamina C','Gastritis','Salsa',14),(15,'Semillas','Proteínas','Favismo','Cocido',15);
/*!40000 ALTER TABLE `usos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `idUsuario` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(45) NOT NULL,
  `contraseña` varchar(45) NOT NULL,
  `fk_empleados` int NOT NULL,
  PRIMARY KEY (`idUsuario`),
  KEY `fk_usuarios_empleados1_idx` (`fk_empleados`),
  CONSTRAINT `fk_usuarios_empleados1` FOREIGN KEY (`fk_empleados`) REFERENCES `empleados` (`idEmpleado`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'crodriguez','pass123',1),(2,'mmorales','pass456',2),(3,'jhuaman','pass789',3),(4,'amejia','pass321',4),(5,'palbornoz','pass654',5),(6,'cflores','pass987',6);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vta_plantas_activas`
--

DROP TABLE IF EXISTS `vta_plantas_activas`;
/*!50001 DROP VIEW IF EXISTS `vta_plantas_activas`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vta_plantas_activas` AS SELECT 
 1 AS `idPlanta`,
 1 AS `nombreCientifico`,
 1 AS `linkImagen`,
 1 AS `nomFamilia`,
 1 AS `nombres_comunes`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vta_plantas_activas`
--

/*!50001 DROP VIEW IF EXISTS `vta_plantas_activas`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vta_plantas_activas` AS select `p`.`idPlanta` AS `idPlanta`,`p`.`nombreCientifico` AS `nombreCientifico`,(select `li`.`linkImagen` from `linksimagenes` `li` where (`li`.`fk_plantas` = `p`.`idPlanta`) limit 1) AS `linkImagen`,`fp`.`nomFamilia` AS `nomFamilia`,group_concat(distinct `nc`.`nombreComun` separator ', ') AS `nombres_comunes` from ((`plantas` `p` join `familias_plantas` `fp` on((`p`.`fk_familiasplantas` = `fp`.`idfamiliaPlanta`))) left join `nombres_comunes` `nc` on((`p`.`idPlanta` = `nc`.`fk_plantas`))) where `p`.`idPlanta` in (select distinct `archivacionesplantas`.`fk_plantas` from `archivacionesplantas`) is false group by `p`.`idPlanta`,`p`.`nombreCientifico`,`fp`.`nomFamilia` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-04 23:20:03
