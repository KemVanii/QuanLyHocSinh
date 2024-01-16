-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: quanlyhocsinh
-- ------------------------------------------------------
-- Server version	8.2.0

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
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `class` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  `size` int NOT NULL,
  `grade_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `grade_id` (`grade_id`),
  CONSTRAINT `class_ibfk_1` FOREIGN KEY (`grade_id`) REFERENCES `grade` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vi_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (18,'10/1',2,1),(19,'10/2',2,1),(20,'10/1',1,1),(21,'11/1',2,2),(22,'10/2',2,1),(23,'10/3',1,1),(24,'11/2',0,2),(25,'11/2',1,2);
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grade`
--

DROP TABLE IF EXISTS `grade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grade` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vi_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grade`
--

LOCK TABLES `grade` WRITE;
/*!40000 ALTER TABLE `grade` DISABLE KEYS */;
INSERT INTO `grade` VALUES (1,'10'),(2,'11'),(3,'12');
/*!40000 ALTER TABLE `grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phone_student`
--

DROP TABLE IF EXISTS `phone_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phone_student` (
  `id` int NOT NULL AUTO_INCREMENT,
  `number` varchar(10) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  `student_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  CONSTRAINT `phone_student_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vi_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phone_student`
--

LOCK TABLES `phone_student` WRITE;
/*!40000 ALTER TABLE `phone_student` DISABLE KEYS */;
/*!40000 ALTER TABLE `phone_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `phone_user`
--

DROP TABLE IF EXISTS `phone_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phone_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `number` varchar(10) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `phone_user_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vi_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `phone_user`
--

LOCK TABLES `phone_user` WRITE;
/*!40000 ALTER TABLE `phone_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `phone_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `score`
--

DROP TABLE IF EXISTS `score`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `score` (
  `id` int NOT NULL AUTO_INCREMENT,
  `value` float DEFAULT NULL,
  `type` varchar(20) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  `score_board_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `score_board_id` (`score_board_id`),
  CONSTRAINT `score_ibfk_1` FOREIGN KEY (`score_board_id`) REFERENCES `score_board` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vi_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `score`
--

LOCK TABLES `score` WRITE;
/*!40000 ALTER TABLE `score` DISABLE KEYS */;
INSERT INTO `score` VALUES (42,7,'15p',109),(43,7,'45p',109),(44,7,'ck',109),(45,5,'15p',113),(46,9,'45p',113),(47,9,'ck',113),(48,8,'15p',111),(49,9,'45p',111),(50,8,'ck',111),(51,9,'15p',115),(52,9,'45p',115),(53,9,'ck',115),(54,0,'15p',117),(55,0,'45p',117),(56,0,'ck',117),(57,7,'15p',121),(58,8,'45p',121),(59,9,'ck',121),(66,8,'15p',120),(67,9,'15p',120),(68,9,'45p',120),(69,9,'ck',120),(70,8,'15p',124),(71,7,'15p',124),(72,7,'45p',124),(73,3,'ck',124),(74,10,'15p',118),(75,10,'45p',118),(76,10,'ck',118),(77,8,'15p',122),(78,8,'45p',122),(79,8,'ck',122),(80,9,'15p',110),(81,9,'45p',110),(82,9,'ck',110),(83,9,'15p',114),(84,9,'45p',114),(85,9,'ck',114),(86,9,'15p',112),(87,9,'45p',112),(88,9,'ck',112),(89,9,'15p',116),(90,9,'45p',116),(91,9,'ck',116),(92,10,'15p',119),(93,10,'45p',119),(94,8,'ck',119),(95,5,'15p',123),(96,9,'45p',123),(97,9,'ck',123),(101,0,'15p',131),(102,0,'45p',131),(103,0,'ck',131),(104,0,'15p',129),(105,0,'45p',129),(106,0,'ck',129),(133,5,'15p',135),(134,5,'45p',135),(135,5,'ck',135),(136,10,'15p',155),(137,10,'45p',155),(138,10,'ck',155),(155,5,'15p',133),(156,5,'45p',133),(157,5,'ck',133),(158,10,'15p',153),(159,10,'45p',153),(160,10,'ck',153);
/*!40000 ALTER TABLE `score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `score_board`
--

DROP TABLE IF EXISTS `score_board`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `score_board` (
  `id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `subject_id` int NOT NULL,
  `class_id` int NOT NULL,
  `semester_id` int NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`),
  KEY `subject_id` (`subject_id`),
  KEY `class_id` (`class_id`),
  KEY `semester_id` (`semester_id`),
  CONSTRAINT `score_board_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`id`),
  CONSTRAINT `score_board_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`),
  CONSTRAINT `score_board_ibfk_3` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`),
  CONSTRAINT `score_board_ibfk_4` FOREIGN KEY (`semester_id`) REFERENCES `semester` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=157 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vi_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `score_board`
--

LOCK TABLES `score_board` WRITE;
/*!40000 ALTER TABLE `score_board` DISABLE KEYS */;
INSERT INTO `score_board` VALUES (109,2,1,18,1,1),(110,2,2,18,1,1),(111,2,1,18,2,1),(112,2,2,18,2,1),(113,3,1,18,1,1),(114,3,2,18,1,1),(115,3,1,18,2,1),(116,3,2,18,2,1),(117,4,1,19,1,1),(118,4,2,19,1,1),(119,4,1,19,2,1),(120,4,2,19,2,1),(121,5,1,19,1,1),(122,5,2,19,1,1),(123,5,1,19,2,1),(124,5,2,19,2,1),(125,6,1,20,3,0),(126,6,2,20,3,0),(127,6,1,20,4,0),(128,6,2,20,4,0),(129,7,1,20,3,1),(130,7,2,20,3,1),(131,7,1,20,4,1),(132,7,2,20,4,1),(133,2,1,21,3,1),(134,2,2,21,3,1),(135,2,1,21,4,1),(136,2,2,21,4,1),(137,3,1,25,3,1),(138,3,2,25,3,1),(139,3,1,25,4,1),(140,3,2,25,4,1),(141,8,1,22,3,1),(142,8,2,22,3,1),(143,8,1,22,4,1),(144,8,2,22,4,1),(145,9,1,22,3,1),(146,9,2,22,3,1),(147,9,1,22,4,1),(148,9,2,22,4,1),(149,10,1,23,3,1),(150,10,2,23,3,1),(151,10,1,23,4,1),(152,10,2,23,4,1),(153,5,1,21,3,1),(154,5,2,21,3,1),(155,5,1,21,4,1),(156,5,2,21,4,1);
/*!40000 ALTER TABLE `score_board` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester`
--

DROP TABLE IF EXISTS `semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `semester` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(10) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vi_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester`
--

LOCK TABLES `semester` WRITE;
/*!40000 ALTER TABLE `semester` DISABLE KEYS */;
INSERT INTO `semester` VALUES (1,'HK1_23-24'),(2,'HK2_23-24'),(3,'HK1_24-25'),(4,'HK2_24-25');
/*!40000 ALTER TABLE `semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  `gender` tinyint(1) NOT NULL,
  `dob` datetime NOT NULL,
  `address` varchar(100) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  `email` varchar(50) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  `status` tinyint(1) NOT NULL,
  `isTransferSchool` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vi_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (2,'Student 2',1,'2001-02-02 00:00:00','TPHCM','student2@gmail.com',1,0),(3,'Student 3',2,'2002-03-03 00:00:00','TPHCM','student3@gmail.com',1,0),(4,'Student 4',1,'2003-04-04 00:00:00','TPHCM','student4@gmail.com',1,0),(5,'Student 5',2,'2004-05-05 00:00:00','TPHCM','student5@gmail.com',1,0),(6,'Student 6',1,'2005-06-06 00:00:00','TPHCM','student6@gmail.com',1,0),(7,'Student 7',2,'2006-07-07 00:00:00','TPHCM','student7@gmail.com',1,0),(8,'Student 8',1,'2007-08-08 00:00:00','TPHCM','student8@gmail.com',1,0),(9,'Student 9',2,'2008-09-09 00:00:00','TPHCM','student9@gmail.com',1,0),(10,'Student 10',1,'2009-10-10 00:00:00','TPHCM','student10@gmail.com',1,0),(11,'Student 11',2,'2010-11-11 00:00:00','TPHCM','student11@gmail.com',1,0),(12,'Student 12',1,'2011-12-12 00:00:00','TPHCM','student12@gmail.com',1,0),(13,'Student 13',2,'2012-01-13 00:00:00','TPHCM','student13@gmail.com',1,0),(14,'Student 14',1,'2013-02-14 00:00:00','TPHCM','student14@gmail.com',1,0),(15,'Student 15',2,'2014-03-15 00:00:00','TPHCM','student15@gmail.com',1,0),(16,'Student 16',1,'2015-04-16 00:00:00','TPHCM','student16@gmail.com',1,0),(17,'Student 17',2,'2016-05-17 00:00:00','TPHCM','student17@gmail.com',1,0),(18,'Student 18',1,'2017-06-18 00:00:00','TPHCM','student18@gmail.com',1,0),(19,'Student 19',2,'2018-07-19 00:00:00','TPHCM','student19@gmail.com',1,0),(20,'Student 20',1,'2019-08-20 00:00:00','TPHCM','hocsinh@gmail.com',1,0),(26,'Test',1,'2008-09-30 00:00:00','TPHCM','hongbao2003@gmail.com',1,0),(27,'Bao Bui',1,'2008-01-14 00:00:00','TPHCM','customer@customer.com',1,0),(28,'chuyển trường 11',1,'2007-05-14 00:00:00','TPHCM','nguoidung7@gmail.com',1,0);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subject` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vi_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES (1,'Toán',1),(2,'Văn',1);
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher_class`
--

DROP TABLE IF EXISTS `teacher_class`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher_class` (
  `id` int NOT NULL AUTO_INCREMENT,
  `teacher_id` int DEFAULT NULL,
  `class_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `teacher_id` (`teacher_id`),
  KEY `class_id` (`class_id`),
  CONSTRAINT `teacher_class_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `user` (`id`),
  CONSTRAINT `teacher_class_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `class` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vi_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher_class`
--

LOCK TABLES `teacher_class` WRITE;
/*!40000 ALTER TABLE `teacher_class` DISABLE KEYS */;
INSERT INTO `teacher_class` VALUES (35,3,18),(36,4,18),(37,3,19),(38,4,19),(39,3,20),(40,4,20),(41,3,21),(42,4,21),(43,3,22),(44,4,22),(45,3,23),(46,4,23),(47,3,24),(48,4,24),(49,3,25),(50,4,25);
/*!40000 ALTER TABLE `teacher_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  `gender` tinyint(1) NOT NULL,
  `dob` datetime NOT NULL,
  `address` varchar(100) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  `password` varchar(100) COLLATE utf8mb4_vi_0900_as_cs NOT NULL,
  `user_role` enum('Teacher','Employee','Admin') COLLATE utf8mb4_vi_0900_as_cs DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `subject_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `subject_id` (`subject_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`subject_id`) REFERENCES `subject` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_vi_0900_as_cs;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Nguyễn VĂn A',1,'1991-01-01 00:00:00','TPHCM','admin','e10adc3949ba59abbe56e057f20f883e','Admin',1,NULL),(2,'Nguyễn Văn B',1,'1991-01-01 00:00:00','TPHCM','nhanvien','e10adc3949ba59abbe56e057f20f883e','Employee',1,NULL),(3,'Nguyễn Văn C',1,'1991-01-01 00:00:00','TPHCM','giaovien','e10adc3949ba59abbe56e057f20f883e','Teacher',1,1),(4,'Nguyễn Văn D',1,'1991-01-01 00:00:00','TPHCM','giaovien2','e10adc3949ba59abbe56e057f20f883e','Teacher',1,2),(5,'Nguyễn Văn GiaoVien',1,'1991-01-01 00:00:00','TPHCM','giaoVien','e10adc3949ba59abbe56e057f20f883e','Teacher',1,NULL);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-14 23:48:27
