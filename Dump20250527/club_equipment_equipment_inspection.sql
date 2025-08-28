-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: club_equipment
-- ------------------------------------------------------
-- Server version	8.0.40

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
-- Table structure for table `equipment_inspection`
--

DROP TABLE IF EXISTS `equipment_inspection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipment_inspection` (
  `inspection_id` int NOT NULL AUTO_INCREMENT,
  `equipment_id` int NOT NULL,
  `inspected_time` datetime NOT NULL,
  `inspection_status` varchar(50) NOT NULL,
  `inspection_notes` text,
  PRIMARY KEY (`inspection_id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipment_inspection`
--

LOCK TABLES `equipment_inspection` WRITE;
/*!40000 ALTER TABLE `equipment_inspection` DISABLE KEYS */;
INSERT INTO `equipment_inspection` VALUES (1,1,'2025-05-26 06:18:22','needs_repair',''),(2,1,'2025-05-26 06:18:34','unusable',''),(3,1,'2025-05-26 06:24:57','needs_repair',''),(4,7,'2025-05-26 06:25:21','normal',''),(5,9,'2025-05-26 09:19:06','needs_repair',''),(6,10,'2025-05-26 09:19:13','unusable',''),(7,7,'2025-05-26 09:20:00','needs_repair',''),(8,9,'2025-05-26 09:20:07','normal',''),(9,7,'2025-05-26 09:20:11','normal',''),(10,5,'2025-05-26 15:22:43','needs_repair',''),(11,6,'2025-05-26 15:23:16','normal',''),(12,10,'2025-05-26 15:24:28','needs_repair',''),(13,4,'2025-05-26 15:28:58','needs_repair','報修原因: 123'),(14,4,'2025-05-26 15:55:59','needs_repair','報修原因: 123'),(15,7,'2025-05-26 15:56:24','needs_repair','報修原因: 123'),(16,7,'2025-05-26 16:00:14','normal',''),(17,2,'2025-05-26 16:00:41','unusable','');
/*!40000 ALTER TABLE `equipment_inspection` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-27  2:36:54
