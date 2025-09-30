CREATE DATABASE  IF NOT EXISTS `autopercepcao_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `autopercepcao_db`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: autopercepcao_db
-- ------------------------------------------------------
-- Server version	8.0.36

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
-- Table structure for table `respostasquestionario`
--

DROP TABLE IF EXISTS `respostasquestionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `respostasquestionario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` varchar(255) NOT NULL,
  `data_submissao` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `resposta_q1` int NOT NULL,
  `resposta_q2` int NOT NULL,
  `resposta_q3` int NOT NULL,
  `pontuacao_total` int NOT NULL,
  `nivel_bem_estar` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `respostasquestionario`
--

LOCK TABLES `respostasquestionario` WRITE;
/*!40000 ALTER TABLE `respostasquestionario` DISABLE KEYS */;
INSERT INTO `respostasquestionario` VALUES (1,'user_teste@email.com','2025-09-30 12:50:08',1,1,1,3,'Atenção'),(2,'user_teste@email.com','2025-09-30 12:53:35',1,1,2,4,'Atenção'),(3,'user_teste@email.com','2025-09-30 12:54:44',1,2,3,6,'Satisfatório'),(4,'user_teste@email.com','2025-09-30 13:40:07',3,3,3,9,'Satisfatório'),(5,'user_teste@email.com','2025-09-30 13:41:02',1,1,1,3,'Atenção'),(6,'user_teste@email.com','2025-09-30 13:48:50',3,3,5,11,'Ótimo'),(7,'user_teste@email.com','2025-09-30 13:49:51',5,2,1,8,'Satisfatório'),(8,'user_teste@email.com','2025-09-30 14:17:34',3,5,3,11,'Ótimo'),(9,'user_teste@email.com','2025-09-30 14:21:10',3,3,5,11,'Ótimo'),(10,'user_teste@email.com','2025-09-30 14:21:48',5,5,5,15,'Ótimo'),(11,'user_teste@email.com','2025-09-30 14:23:05',2,1,1,4,'Atenção'),(12,'user_teste@email.com','2025-09-30 14:24:48',3,2,1,6,'Satisfatório');
/*!40000 ALTER TABLE `respostasquestionario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-30 12:26:02
