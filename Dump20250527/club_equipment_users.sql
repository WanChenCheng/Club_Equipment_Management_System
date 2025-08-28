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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(50) NOT NULL,
  `password` varchar(512) NOT NULL,
  `credit_score` int DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `user_role` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'222','pbkdf2:sha1:1000000$waLi3D1eRHidtwhr$1af8f8f31c373b1d38ab01a7f131dcdf221798b0',50,'222@gmail','user'),(3,'333','pbkdf2:sha1:1000000$PnhBHWPrRSKzwbhs$ac11bbb86b3887dcdce9aba7aedb13b784415a09',100,'333@gmail.com','user'),(4,'222','pbkdf2:sha1:1000000$JaYRkyDeEQ4dyN8i$291c4e3ff829aae9e99451692b4d74c2d3317413',NULL,'222@gmail',NULL),(5,'555','pbkdf2:sha1:1000000$hdxgrExiZhfqxeJS$3456be856dd099e32bdb56f6234bfab64bce297d',NULL,'555@gmail.com',NULL),(6,'666','pbkdf2:sha1:1000000$IQv21165d0Rc2jli$e45c55f9cadad4b29998c92cfe3beb11048b5ff1',NULL,'666@gmail.com',NULL),(7,'777','pbkdf2:sha1:1000000$eftCcMgedsc6mQwL$65ca0f8828d9217a841f97cf04c5aa53382176f2',NULL,'777@gmail',NULL),(8,'888','pbkdf2:sha1:1000000$k59vOysAo0W12RMu$f7d7a185ef10ca03aeb77cd0a7466fe5858fb222',NULL,'888@gmail',NULL),(9,'999','pbkdf2:sha1:1000000$6FcOYtDoBCphvHYJ$9ccc0c748f5ca721e7f3a175dc5f4954752c34e7',NULL,'999@gmail',NULL),(10,'444','pbkdf2:sha1:1000000$ZOVKTApETuJIhEwo$a13b04e544a1e01ee94b64e34fdce3766b8a1223',NULL,'444@gmail',NULL),(11,'11','pbkdf2:sha1:1000000$AjCIEUB09BzMfm2v$578a87fb112e6b7943009f4f1f1bf34e1f074eb7',NULL,'11@gmail',NULL),(12,'22','pbkdf2:sha1:1000000$4JWDLGRscIxolMfE$fa0aee36e3e3c3df226e9b4049533474367d1967',80,'22@gmail','user'),(13,'33','pbkdf2:sha1:1000000$XX79DnakgZYl7u2h$57d3eb764730ad7aec3c7dad9376d0d347477e25',100,'33@gmail','user'),(14,'55','pbkdf2:sha1:1000000$7r1EHwLf9WOVfcy7$5529dad299cd2decf25a1990f419cf7adff7c113',NULL,'55@gmail','user'),(15,'66','pbkdf2:sha1:1000000$dCdY9PraAgnLRZvT$f9d42301828ffe12df8ef26ac54bb9cd29f81887',NULL,'66@gmail',NULL),(16,'77','pbkdf2:sha1:1000000$0oaYgGDbSY9PUUMg$b42ba0b1986c39b69d6fc92d280eee0003b98a6a',NULL,'77@gmail',NULL),(17,'88','pbkdf2:sha1:1000000$QQIFdoEsCZLukFyt$11f6582c38af4428cad4ebcedb288110736b06e2',NULL,'88@gmail',NULL),(18,'99','pbkdf2:sha1:1000000$hSzgf4eCu8wQYgOs$11cd510a3fb6ef4e4a484fb0b2daa1ece1ce2b9c',NULL,'99@gmail','admin'),(19,'12','pbkdf2:sha256:1000000$NXAhjcpjdrDx2Q8K$0902513495d0101df49f94fa5de03b595be4f7abcc3d2b992baf4914b70dd274',NULL,'12@gmail','admin'),(21,'吉他','pbkdf2:sha256:1000000$mtwIfNUDpfPIK9aM$07c4a589960c89535306ae95b8d55e4bddba575d3037c46f8e9bdadca7f43b8d',NULL,'12@gmail','admin'),(22,'吉他','pbkdf2:sha256:1000000$fWTRc2Wwphfk0wrm$25b157fb70c0211500d95e07a0ba89b61ec9c1ec0acd4468f99be81022ec9e32',NULL,'12@gmail','admin'),(23,'124','pbkdf2:sha256:1000000$p3XoosAo6twABxYL$0e0eddd91d192b871371738db930cb2641c17d2dd7d187a93316b495f70fb54c',NULL,'124@gmail','admin'),(25,'862','pbkdf2:sha256:1000000$mF1DD9OLH6xN0Lqz$1b9ae3c955cb36ce5b6dd12cc95dae0c935f97ff4b8feab2923ad52a4aa68dc7',NULL,'862@gmail','user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
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
