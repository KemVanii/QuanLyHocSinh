-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: quanlyhocsinh
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Dumping data for table `class`
--

LOCK TABLES `class` WRITE;
/*!40000 ALTER TABLE `class` DISABLE KEYS */;
INSERT INTO `class` VALUES (1,'10A7',40,1),(2,'11B4',40,2);
/*!40000 ALTER TABLE `class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `grade`
--

LOCK TABLES `grade` WRITE;
/*!40000 ALTER TABLE `grade` DISABLE KEYS */;
INSERT INTO `grade` VALUES (1,'10'),(2,'11'),(3,'12');
/*!40000 ALTER TABLE `grade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `phone`
--

LOCK TABLES `phone` WRITE;
/*!40000 ALTER TABLE `phone` DISABLE KEYS */;
/*!40000 ALTER TABLE `phone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `score`
--

LOCK TABLES `score` WRITE;
/*!40000 ALTER TABLE `score` DISABLE KEYS */;
INSERT INTO `score` VALUES (1,7.5,'15p',1),(2,6,'15p',1),(3,3,'1',1),(4,7,'1',2),(5,4,'15p',3),(6,6.7,'1',2),(7,4.5,'15p',2),(8,9,'15p',3),(9,8,'1',3),(10,6,'1',1),(11,6,'1',3),(12,9,'15',2),(13,3,'1',4),(14,4,'1',2),(15,7.5,'15p',5),(16,3.4,'15p',6),(17,6.3,'1',5),(18,8.9,'1',5),(19,7.7,'15p',6),(20,5.5,'15p',6);
/*!40000 ALTER TABLE `score` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `score_board`
--

LOCK TABLES `score_board` WRITE;
/*!40000 ALTER TABLE `score_board` DISABLE KEYS */;
INSERT INTO `score_board` VALUES (1,1,1,1,1,1),(2,2,1,1,1,1);
/*!40000 ALTER TABLE `score_board` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `semester`
--

LOCK TABLES `semester` WRITE;
/*!40000 ALTER TABLE `semester` DISABLE KEYS */;
INSERT INTO `semester` VALUES (1,'HK1_23-24');
/*!40000 ALTER TABLE `semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'Student 1',1,'2000-01-01 00:00:00','TPHCM'),(2,'Student 2',0,'2001-02-02 00:00:00','TPHCM'),(3,'Student 3',1,'2002-03-03 00:00:00','TPHCM'),(4,'Student 4',0,'2003-04-04 00:00:00','TPHCM'),(5,'Student 5',1,'2004-05-05 00:00:00','TPHCM'),(6,'Student 6',0,'2005-06-06 00:00:00','TPHCM'),(7,'Student 7',1,'2006-07-07 00:00:00','TPHCM'),(8,'Student 8',0,'2007-08-08 00:00:00','TPHCM'),(9,'Student 9',1,'2008-09-09 00:00:00','TPHCM'),(10,'Student 10',0,'2009-10-10 00:00:00','TPHCM'),(11,'Student 11',1,'2010-11-11 00:00:00','TPHCM'),(12,'Student 12',0,'2011-12-12 00:00:00','TPHCM'),(13,'Student 13',1,'2012-01-13 00:00:00','TPHCM'),(14,'Student 14',0,'2013-02-14 00:00:00','TPHCM'),(15,'Student 15',1,'2014-03-15 00:00:00','TPHCM'),(16,'Student 16',0,'2015-04-16 00:00:00','TPHCM'),(17,'Student 17',1,'2016-05-17 00:00:00','TPHCM'),(18,'Student 18',0,'2017-06-18 00:00:00','TPHCM'),(19,'Student 19',1,'2018-07-19 00:00:00','TPHCM'),(20,'Student 20',0,'2019-08-20 00:00:00','TPHCM'),(21,'Tu Tran',1,'2003-07-17 00:00:00','481/15 Nguyen Van Qua'),(22,'Ly',0,'2024-09-22 20:52:00','481/15 Nguyen Van Qua');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES (1,'Toán',1);
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `teacher_class`
--

LOCK TABLES `teacher_class` WRITE;
/*!40000 ALTER TABLE `teacher_class` DISABLE KEYS */;
/*!40000 ALTER TABLE `teacher_class` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'Nguyễn Văn Admin',1,'1991-01-01 00:00:00','TPHCM','admin','e10adc3949ba59abbe56e057f20f883e','Admin',1,1),(2,'nhanvien',0,'2024-01-07 14:05:00','dwa','Ly','e10adc3949ba59abbe56e057f20f883e','Employee',1,1),(3,'giaovien',0,'2024-01-07 14:05:00','dwa','giaovien','e10adc3949ba59abbe56e057f20f883e','Teacher',1,1);
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

-- Dump completed on 2024-01-07 17:03:05
