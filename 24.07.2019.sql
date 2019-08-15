-- MySQL dump 10.13  Distrib 5.7.26, for Linux (x86_64)
--
-- Host: localhost    Database: django_db
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `app_card`
--

DROP TABLE IF EXISTS `app_card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_card` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data` varchar(200) NOT NULL,
  `partner_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `data` (`data`),
  KEY `app_card_partner_id_60fe2f16_fk_app_partner_id` (`partner_id`),
  CONSTRAINT `app_card_partner_id_60fe2f16_fk_app_partner_id` FOREIGN KEY (`partner_id`) REFERENCES `app_partner` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_card`
--

LOCK TABLES `app_card` WRITE;
/*!40000 ALTER TABLE `app_card` DISABLE KEYS */;
INSERT INTO `app_card` VALUES (2,'0000C1813B344F',1),(3,'000088043C3787',1),(4,'00008C444C79FD',5),(5,'0000EA4A442ECA',6);
/*!40000 ALTER TABLE `app_card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_contractor`
--

DROP TABLE IF EXISTS `app_contractor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_contractor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `UNP` varchar(50) NOT NULL,
  `address` varchar(50) NOT NULL,
  `balance` decimal(7,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_contractor`
--

LOCK TABLES `app_contractor` WRITE;
/*!40000 ALTER TABLE `app_contractor` DISABLE KEYS */;
INSERT INTO `app_contractor` VALUES (2,'ООО \"ЕВРОТОРГ\"','101168744','г. Минск,ул. Казинца, д.52а, ком. 22',80.25),(3,'СООО \"ПЕРФЕКТ\"','800015378','Брестская обл.,г. Брест,ул. Гвардейская, д.23',349.25),(4,'ОАО \"БСТ\"','200274653','Брестская обл.,г. Брест,ул. Купалы Я., д.19в',12.00),(5,'ООО \"ТАКСИ 184\"','191476628','г. Минск,ул. Нововиленская, д.48, оф. 3',200.00),(6,'ООО \"Такси 5\"','192383104','г. Минск,ул. Стрелковая, д.14, каб. 29',0.00),(7,'ООО \"ТАКС 007\"','193147563','г. Минск,ул. Маяковского, д.146, оф. 14',1.00),(8,'ООО \"ТАКС 007\"','193147563','г. Минск,уsл. Маяковского, д.146, оф. 14',1.00),(9,'Егор','123456789','1',0.00);
/*!40000 ALTER TABLE `app_contractor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_partner`
--

DROP TABLE IF EXISTS `app_partner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_partner` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `identification_type` smallint(5) unsigned NOT NULL,
  `data` varchar(200) NOT NULL,
  `balance` decimal(7,2) NOT NULL,
  `contractor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_partner_contractor_id_47da1f21_fk_app_contractor_id` (`contractor_id`),
  CONSTRAINT `app_partner_contractor_id_47da1f21_fk_app_contractor_id` FOREIGN KEY (`contractor_id`) REFERENCES `app_contractor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_partner`
--

LOCK TABLES `app_partner` WRITE;
/*!40000 ALTER TABLE `app_partner` DISABLE KEYS */;
INSERT INTO `app_partner` VALUES (1,'ЗАО «Интернет-магазин Евроопт»',3,'УНП 691536217, юридический адрес: 220019 Минская область, Минский район, Щомыслицкий с/с, Западный промузел, ТЭЦ-4  кабинет 229.',114.00,2),(3,'Директор СООО ПЕРФЕКТ',2,'Фамилия Имя Отчество',190.00,3),(5,'Эпольсофт',1,'21312',99.25,3),(6,'Егор',1,'1234',110.00,9);
/*!40000 ALTER TABLE `app_partner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_payment`
--

DROP TABLE IF EXISTS `app_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `annotation` varchar(150) NOT NULL,
  `date` datetime(6) NOT NULL,
  `contractor_id` int(11) DEFAULT NULL,
  `amount` decimal(7,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_payment_contractor_id_03ac8458_fk_app_contractor_id` (`contractor_id`),
  CONSTRAINT `app_payment_contractor_id_03ac8458_fk_app_contractor_id` FOREIGN KEY (`contractor_id`) REFERENCES `app_contractor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_payment`
--

LOCK TABLES `app_payment` WRITE;
/*!40000 ALTER TABLE `app_payment` DISABLE KEYS */;
INSERT INTO `app_payment` VALUES (13,'2','2019-05-28 15:14:56.795505',2,100.00),(14,'1','2019-05-29 08:57:13.314458',3,10.00),(15,'по платежу какому-то','2019-05-29 20:09:36.799832',3,20.00),(16,'ну нужно','2019-05-29 20:10:42.577981',3,2.00),(17,'wqe','2019-05-30 08:00:04.132981',3,100.00),(18,'kj','2019-05-30 11:36:12.572465',3,100.50),(19,'','2019-06-03 14:17:57.649400',5,100.00),(20,'','2019-06-04 10:01:45.246919',2,100.00),(21,'','2019-07-04 08:02:21.878105',9,100.00);
/*!40000 ALTER TABLE `app_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_post`
--

DROP TABLE IF EXISTS `app_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `post_id` smallint(5) unsigned NOT NULL,
  `mac_uid` varchar(12) NOT NULL,
  `station_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mac_uid` (`mac_uid`),
  KEY `app_post_station_id_6dc2180c_fk_app_station_id` (`station_id`),
  CONSTRAINT `app_post_station_id_6dc2180c_fk_app_station_id` FOREIGN KEY (`station_id`) REFERENCES `app_station` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_post`
--

LOCK TABLES `app_post` WRITE;
/*!40000 ALTER TABLE `app_post` DISABLE KEYS */;
INSERT INTO `app_post` VALUES (1,1,'B827EBDED3CB',1),(2,2,'1234567890',1),(3,3,'1234567891',1);
/*!40000 ALTER TABLE `app_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_station`
--

DROP TABLE IF EXISTS `app_station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_station` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `station_id` int(11) NOT NULL,
  `owner` varchar(50) NOT NULL,
  `info` longtext NOT NULL,
  `course` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_station`
--

LOCK TABLES `app_station` WRITE;
/*!40000 ALTER TABLE `app_station` DISABLE KEYS */;
INSERT INTO `app_station` VALUES (1,1,'ИП ИВАНОВ И.И.','ТАА \"М-Пласт\"\r\nТаварыства з абмежаванай адказнасцю \"М-Пласт\"\r\nМ-Пласт',2),(3,2,'ИП Петров П.П.','какая-то инфа',1);
/*!40000 ALTER TABLE `app_station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_transaction`
--

DROP TABLE IF EXISTS `app_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_transaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_time` datetime(6) NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `initiator_type` smallint(5) unsigned NOT NULL,
  `card_id` int(11) NOT NULL,
  `partner_id` int(11) NOT NULL,
  `post_id` int(11) NOT NULL,
  `station_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_transaction_card_id_19a4cac7_fk_app_card_id` (`card_id`),
  KEY `app_transaction_post_id_2b208bc7_fk_app_post_id` (`post_id`),
  KEY `app_transaction_station_id_04996457_fk_app_station_id` (`station_id`),
  KEY `app_transaction_partner_id_9c96f576_fk_app_partner_id` (`partner_id`),
  CONSTRAINT `app_transaction_card_id_19a4cac7_fk_app_card_id` FOREIGN KEY (`card_id`) REFERENCES `app_card` (`id`),
  CONSTRAINT `app_transaction_partner_id_9c96f576_fk_app_partner_id` FOREIGN KEY (`partner_id`) REFERENCES `app_partner` (`id`),
  CONSTRAINT `app_transaction_post_id_2b208bc7_fk_app_post_id` FOREIGN KEY (`post_id`) REFERENCES `app_post` (`id`),
  CONSTRAINT `app_transaction_station_id_04996457_fk_app_station_id` FOREIGN KEY (`station_id`) REFERENCES `app_station` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_transaction`
--

LOCK TABLES `app_transaction` WRITE;
/*!40000 ALTER TABLE `app_transaction` DISABLE KEYS */;
INSERT INTO `app_transaction` VALUES (8,'2019-05-22 19:31:56.304934',5.00,0,2,3,1,1),(9,'2019-05-22 19:39:32.039581',5.00,0,2,3,1,1),(11,'2019-05-28 22:29:32.000000',1.00,0,2,3,1,1),(13,'2019-05-28 22:35:59.000000',0.00,0,2,3,1,1),(14,'2019-05-28 22:43:40.000000',1.00,0,2,3,1,1),(15,'2019-05-28 23:04:49.000000',1.00,0,2,3,1,1),(16,'2019-05-28 23:05:37.000000',9.00,0,2,3,1,1),(66,'2019-06-04 07:24:36.000000',1.00,0,2,3,1,1),(67,'2019-06-04 08:17:01.000000',2.00,0,2,3,1,1),(68,'2019-06-04 08:17:39.000000',3.00,0,2,3,1,1),(69,'2019-06-04 08:18:49.000000',10.00,0,2,3,1,1),(70,'2019-06-04 08:30:04.000000',2.00,0,2,3,1,1),(71,'2019-06-30 11:02:54.000000',1.00,0,4,1,1,1),(75,'2019-07-15 10:13:45.000000',1.00,0,4,5,1,1),(76,'2019-07-20 05:15:11.000000',1.00,0,5,6,1,1),(77,'2019-07-20 05:20:56.000000',2.00,0,5,6,1,1),(78,'2019-07-20 05:25:57.000000',1.00,0,5,6,1,1),(79,'2019-07-20 05:31:57.000000',2.00,0,5,6,1,1),(80,'2019-07-21 17:30:49.000000',1.00,0,5,6,1,1),(81,'2019-07-21 17:37:46.000000',3.00,0,5,6,1,1);
/*!40000 ALTER TABLE `app_transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `app_usertransaction`
--

DROP TABLE IF EXISTS `app_usertransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `app_usertransaction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` decimal(7,2) NOT NULL,
  `date_pub` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  `annotation` varchar(150) NOT NULL,
  `exec_type` smallint(6) NOT NULL,
  `entity` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_usertransaction_user_id_f9281754_fk_auth_user_id` (`user_id`),
  CONSTRAINT `app_usertransaction_user_id_f9281754_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `app_usertransaction`
--

LOCK TABLES `app_usertransaction` WRITE;
/*!40000 ALTER TABLE `app_usertransaction` DISABLE KEYS */;
INSERT INTO `app_usertransaction` VALUES (21,2.00,'2019-05-29 17:39:07.366602',1,'Изменение баланса клиента. Успешно. Добавлено 2 к Эпольсофт',1,'Клиент: Эпольсофт'),(22,300.00,'2019-05-29 17:45:11.944004',1,'Изменение баланса клиента. Успешно. Добавлено 300 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(23,100.00,'2019-05-29 17:45:15.650616',1,'Ошибка! Вы добавили больше, чем имеется у контрагента',0,'Клиент: Директор СООО ПЕРФЕКТ'),(24,-50.00,'2019-05-29 17:45:24.440398',1,'Изменение баланса клиента. Ошибка. У партнера не может быть меньше нуля',0,'Клиент: Эпольсофт'),(25,-300.00,'2019-05-29 17:45:35.646254',1,'Изменение баланса клиента. Успешно. Добавлено -300 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(26,35.00,'2019-05-29 17:45:40.396256',1,'Изменение баланса клиента. Успешно. Добавлено 35 к ЗАО «Интернет-магазин Евроопт»',1,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(27,2.00,'2019-05-29 20:10:42.597119',1,'Добавление платежа. Успешно. Платеж для \"СООО \"ПЕРФЕКТ\"\" добавлен с примечанием: \"ну нужно\"',1,'Контрагент: СООО \"ПЕРФЕКТ\"'),(28,2.00,'2019-05-29 20:30:28.974068',1,'Изменение баланса клиента. Успешно. Добавлено 2 к Эпольсофт',1,'Клиент: Эпольсофт'),(29,2.00,'2019-05-29 20:30:30.822379',1,'Изменение баланса клиента. Успешно. Добавлено 2 к Эпольсофт',1,'Клиент: Эпольсофт'),(30,2.00,'2019-05-29 20:30:37.509106',1,'Изменение баланса клиента. Успешно. Добавлено 2 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(31,2.00,'2019-05-29 20:30:39.387999',1,'Изменение баланса клиента. Успешно. Добавлено 2 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(32,2.00,'2019-05-29 20:30:41.308652',1,'Изменение баланса клиента. Успешно. Добавлено 2 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(33,2.00,'2019-05-29 20:30:42.677155',1,'Изменение баланса клиента. Успешно. Добавлено 2 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(34,2.00,'2019-05-29 20:30:44.395454',1,'Изменение баланса клиента. Успешно. Добавлено 2 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(35,2.00,'2019-05-29 20:30:46.251545',1,'Изменение баланса клиента. Успешно. Добавлено 2 к Эпольсофт',1,'Клиент: Эпольсофт'),(36,2.00,'2019-05-29 20:30:48.456505',1,'Изменение баланса клиента. Успешно. Добавлено 2 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(37,2.00,'2019-05-29 20:30:50.980705',1,'Изменение баланса клиента. Успешно. Добавлено 2 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(38,32.00,'2019-05-29 20:30:54.364445',1,'Изменение баланса клиента. Успешно. Добавлено 32 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(39,-40.00,'2019-05-29 20:30:58.923388',1,'Изменение баланса клиента. Успешно. Добавлено -40 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(40,23.00,'2019-05-29 20:31:06.283662',1,'Изменение баланса клиента. Успешно. Добавлено 23 к Эпольсофт',1,'Клиент: Эпольсофт'),(41,-30.00,'2019-05-29 20:31:10.620295',1,'Изменение баланса клиента. Успешно. Добавлено -30 к Эпольсофт',1,'Клиент: Эпольсофт'),(42,-50.00,'2019-05-29 20:31:32.967721',1,'Изменение баланса клиента. Ошибка. У партнера не может быть меньше нуля',0,'Клиент: Эпольсофт'),(43,-10.00,'2019-05-29 20:31:37.506453',1,'Изменение баланса клиента. Ошибка. У партнера не может быть меньше нуля',0,'Клиент: Директор СООО ПЕРФЕКТ'),(44,500.00,'2019-05-29 20:31:41.928116',1,'Ошибка! Вы добавили больше, чем имеется у контрагента',0,'Клиент: Эпольсофт'),(45,100.00,'2019-05-29 20:48:25.493846',1,'Изменение баланса клиента. Ошибка! Вы добавили больше, чем имеется у контрагента',0,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(46,100.00,'2019-05-30 08:00:04.142890',1,'Добавление платежа. Успешно. Платеж для \"СООО \"ПЕРФЕКТ\"\" добавлен с примечанием: \"wqe\"',1,'Контрагент: СООО \"ПЕРФЕКТ\"'),(47,100.50,'2019-05-30 11:36:12.592211',1,'Добавление платежа. Успешно. Платеж для \"СООО \"ПЕРФЕКТ\"\" добавлен с примечанием: \"kj\"',1,'Контрагент: СООО \"ПЕРФЕКТ\"'),(48,100.50,'2019-05-30 11:36:27.775983',1,'Изменение баланса клиента. Успешно. Добавлено 100.5 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(49,-50.00,'2019-05-30 11:36:32.983651',1,'Изменение баланса клиента. Ошибка. У партнера не может быть меньше нуля',0,'Клиент: Эпольсофт'),(50,100.00,'2019-05-30 11:36:37.737067',1,'Изменение баланса клиента. Успешно. Добавлено 100 к Эпольсофт',1,'Клиент: Эпольсофт'),(51,1.00,'2019-05-31 07:14:22.323695',1,'Изменение баланса клиента. Успешно. Добавлено 1 к ЗАО «Интернет-магазин Евроопт»',1,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(52,100.00,'2019-06-03 14:17:57.658054',2,'Добавление платежа. Успешно. Платеж для \"ООО \"ТАКСИ 184\"\" добавлен с примечанием: \"\"',1,'Контрагент: ООО \"ТАКСИ 184\"'),(53,9.00,'2019-06-04 00:04:00.532936',2,'Изменение баланса клиента. Успешно. Добавлено 9 к ЗАО «Интернет-магазин Евроопт»',1,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(54,100.00,'2019-06-04 10:01:45.267007',2,'Добавление платежа. Успешно. Платеж для \"ООО \"ЕВРОТОРГ\"\" добавлен с примечанием: \"\"',1,'Контрагент: ООО \"ЕВРОТОРГ\"'),(55,100.00,'2019-06-04 10:02:03.565504',2,'Изменение баланса клиента. Успешно. Добавлено 100 к ЗАО «Интернет-магазин Евроопт»',1,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(56,34.00,'2019-06-05 16:27:07.599550',1,'Изменение баланса клиента. Ошибка! Вы добавили больше, чем имеется у контрагента',0,'Клиент: Егор'),(57,144.00,'2019-06-06 06:52:38.031071',1,'Изменение баланса клиента. Успешно. Добавлено 144 к Эпольсофт',1,'Клиент: Эпольсофт'),(58,-288.00,'2019-06-06 06:52:51.281515',1,'Изменение баланса клиента. Успешно. Добавлено -288 к Эпольсофт',1,'Клиент: Эпольсофт'),(59,100.00,'2019-06-07 06:32:55.900771',2,'Изменение баланса клиента. Успешно. Добавлено 100 к Директор СООО ПЕРФЕКТ',1,'Клиент: Директор СООО ПЕРФЕКТ'),(60,100.00,'2019-06-07 06:33:08.518406',2,'Изменение баланса клиента. Успешно. Добавлено 100 к Эпольсофт',1,'Клиент: Эпольсофт'),(61,0.25,'2019-06-30 06:42:44.334168',2,'Изменение баланса клиента. Успешно. Добавлено 0.25 к ЗАО «Интернет-магазин Евроопт»',1,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(62,0.25,'2019-06-30 06:43:32.445735',2,'Изменение баланса клиента. Успешно. Добавлено 0.25 к ЗАО «Интернет-магазин Евроопт»',1,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(63,-1.00,'2019-06-30 06:44:18.502560',2,'Изменение баланса клиента. Успешно. Добавлено -1 к ЗАО «Интернет-магазин Евроопт»',1,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(64,-29.75,'2019-06-30 06:44:30.016870',2,'Изменение баланса клиента. Успешно. Добавлено -29.75 к ЗАО «Интернет-магазин Евроопт»',1,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(65,-90.00,'2019-06-30 06:44:50.686239',2,'Изменение баланса клиента. Успешно. Добавлено -90 к ЗАО «Интернет-магазин Евроопт»',1,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(66,-79.50,'2019-06-30 06:46:39.609748',2,'Изменение баланса клиента. Успешно. Добавлено -79.5 к ЗАО «Интернет-магазин Евроопт»',1,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(67,20.00,'2019-06-30 11:00:50.977585',2,'Изменение баланса клиента. Успешно. Добавлено 20 к ЗАО «Интернет-магазин Евроопт»',1,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(68,20.00,'2019-06-30 11:34:54.549960',2,'Изменение баланса клиента. Успешно. Добавлено 20 к Егор',1,'Клиент: Егор'),(69,100.00,'2019-06-30 19:33:34.200139',2,'Изменение баланса клиента. Успешно. Добавлено 100 к ЗАО «Интернет-магазин Евроопт»',1,'Клиент: ЗАО «Интернет-магазин Евроопт»'),(70,100.00,'2019-07-04 08:02:21.888538',2,'Добавление платежа. Успешно. Платеж для \"Егор\" добавлен с примечанием: \"\"',1,'Контрагент: Егор'),(71,100.00,'2019-07-04 08:03:10.482486',2,'Изменение баланса клиента. Успешно. Добавлено 100 к Егор',1,'Клиент: Егор');
/*!40000 ALTER TABLE `app_usertransaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add card',7,'add_card'),(26,'Can change card',7,'change_card'),(27,'Can delete card',7,'delete_card'),(28,'Can view card',7,'view_card'),(29,'Can add contractor',8,'add_contractor'),(30,'Can change contractor',8,'change_contractor'),(31,'Can delete contractor',8,'delete_contractor'),(32,'Can view contractor',8,'view_contractor'),(33,'Can add partner',9,'add_partner'),(34,'Can change partner',9,'change_partner'),(35,'Can delete partner',9,'delete_partner'),(36,'Can view partner',9,'view_partner'),(37,'Can add post',10,'add_post'),(38,'Can change post',10,'change_post'),(39,'Can delete post',10,'delete_post'),(40,'Can view post',10,'view_post'),(41,'Can add station',11,'add_station'),(42,'Can change station',11,'change_station'),(43,'Can delete station',11,'delete_station'),(44,'Can view station',11,'view_station'),(45,'Can add transaction',12,'add_transaction'),(46,'Can change transaction',12,'change_transaction'),(47,'Can delete transaction',12,'delete_transaction'),(48,'Can view transaction',12,'view_transaction'),(49,'Can add payment',13,'add_payment'),(50,'Can change payment',13,'change_payment'),(51,'Can delete payment',13,'delete_payment'),(52,'Can view payment',13,'view_payment'),(53,'Can add user transaction',14,'add_usertransaction'),(54,'Can change user transaction',14,'change_usertransaction'),(55,'Can delete user transaction',14,'delete_usertransaction'),(56,'Can view user transaction',14,'view_usertransaction');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$150000$Tz6jXht1DMe8$cV9734GOrOX4A7+cJIpPGWd10hqIRjCjQcD2rsseCXE=','2019-07-09 11:40:42.331746',1,'root','','','',1,1,'2019-05-21 12:10:45.750067'),(2,'pbkdf2_sha256$150000$DxMFIpjOeyhf$C9sRuaQOwJ8lug/5foQeqlybjRgymvlZZ3z4OYYf1ts=','2019-07-19 14:19:35.388595',0,'test','','','',1,1,'2019-05-29 10:34:07.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2019-05-21 12:11:10.054997','1','авав',3,'',8,1),(2,'2019-05-21 12:31:29.892941','1','1',1,'[{\"added\": {}}]',10,1),(3,'2019-05-21 12:32:04.074549','1','000000EA4A442E',1,'[{\"added\": {}}]',7,1),(4,'2019-05-21 12:32:20.322572','2','000000C1813B34',1,'[{\"added\": {}}]',7,1),(5,'2019-05-21 12:32:53.223000','3','0000008C444C79',1,'[{\"added\": {}}]',7,1),(6,'2019-05-27 19:31:08.903663','1','ИП ИВАНОВ И.И.',2,'[{\"changed\": {\"fields\": [\"course\"]}}]',11,1),(7,'2019-05-29 10:34:07.903468','2','test',1,'[{\"added\": {}}]',4,1),(8,'2019-05-29 10:34:21.195297','2','test',2,'[{\"changed\": {\"fields\": [\"is_staff\"]}}]',4,1),(9,'2019-05-30 15:46:46.839636','1','ИП ИВАНОВ И.И.',2,'[{\"changed\": {\"fields\": [\"course\"]}}]',11,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(7,'app','card'),(8,'app','contractor'),(9,'app','partner'),(13,'app','payment'),(10,'app','post'),(11,'app','station'),(12,'app','transaction'),(14,'app','usertransaction'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2019-05-21 12:08:25.198097'),(2,'auth','0001_initial','2019-05-21 12:08:25.637284'),(3,'admin','0001_initial','2019-05-21 12:08:27.327330'),(4,'admin','0002_logentry_remove_auto_add','2019-05-21 12:08:27.708361'),(5,'admin','0003_logentry_add_action_flag_choices','2019-05-21 12:08:27.717733'),(6,'app','0001_initial','2019-05-21 12:08:28.440024'),(7,'contenttypes','0002_remove_content_type_name','2019-05-21 12:08:30.038054'),(8,'auth','0002_alter_permission_name_max_length','2019-05-21 12:08:30.223389'),(9,'auth','0003_alter_user_email_max_length','2019-05-21 12:08:30.411727'),(10,'auth','0004_alter_user_username_opts','2019-05-21 12:08:30.428817'),(11,'auth','0005_alter_user_last_login_null','2019-05-21 12:08:30.559436'),(12,'auth','0006_require_contenttypes_0002','2019-05-21 12:08:30.568863'),(13,'auth','0007_alter_validators_add_error_messages','2019-05-21 12:08:30.585964'),(14,'auth','0008_alter_user_username_max_length','2019-05-21 12:08:30.765479'),(15,'auth','0009_alter_user_last_name_max_length','2019-05-21 12:08:30.951385'),(16,'auth','0010_alter_group_name_max_length','2019-05-21 12:08:31.136758'),(17,'auth','0011_update_proxy_permissions','2019-05-21 12:08:31.159226'),(18,'sessions','0001_initial','2019-05-21 12:08:31.241724'),(19,'app','0002_auto_20190523_1206','2019-05-23 09:07:06.116151'),(20,'app','0003_payment_amount','2019-05-23 09:14:43.971577'),(21,'app','0004_auto_20190523_1306','2019-05-23 10:06:58.596102'),(22,'app','0005_auto_20190527_2149','2019-05-27 18:49:42.142493'),(23,'app','0006_auto_20190527_2242','2019-05-27 19:42:21.239098'),(24,'app','0007_usertransaction','2019-05-29 11:10:46.565273'),(25,'app','0008_auto_20190529_1443','2019-05-29 11:45:36.163892'),(26,'app','0009_auto_20190529_1507','2019-05-29 12:07:13.955464'),(27,'app','0010_auto_20190529_1646','2019-05-29 13:46:40.619086'),(28,'app','0011_auto_20190529_2032','2019-05-29 17:32:29.653273'),(29,'app','0012_auto_20190529_2349','2019-05-29 20:50:01.942875');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1s85wt3t7dlcq20y8d6olz687p5ssl35','ZjFkMTA1MWQ1NDkyMTcyNjQ0ZDRkOGM4YjI0Y2IwZjYxYjIzY2Q2NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTM5MTc2OWMzMTk5ZjNkNDAyYzA5OWFjMzBmMjkzNThmNTNjMjMwIn0=','2019-07-13 05:38:29.330641'),('39uxkpusk9kbl8ll03k1mabfs0xtk760','ZjFkMTA1MWQ1NDkyMTcyNjQ0ZDRkOGM4YjI0Y2IwZjYxYjIzY2Q2NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTM5MTc2OWMzMTk5ZjNkNDAyYzA5OWFjMzBmMjkzNThmNTNjMjMwIn0=','2019-08-02 14:19:35.411876'),('4op2qwby8uwmsm0jn8mmp4l7tli80ixq','ZjFkMTA1MWQ1NDkyMTcyNjQ0ZDRkOGM4YjI0Y2IwZjYxYjIzY2Q2NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTM5MTc2OWMzMTk5ZjNkNDAyYzA5OWFjMzBmMjkzNThmNTNjMjMwIn0=','2019-07-14 19:30:34.426481'),('50f0amyif3dfb8bjp0lkh27p0c8yvj8d','YmNjMDlhOTIxMTIzNjk4ZTAyOTA1NmZiOWViYWE5MTRkMjY3OWUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYTA5OGZlNjZjNjk3MTg3MDFlM2M2ZTQ2MmYzNjY5YzA5NjViOWFkIn0=','2019-06-10 19:30:39.172254'),('ahtxq0e994420knsls0lzl2hre5rlhca','YmNjMDlhOTIxMTIzNjk4ZTAyOTA1NmZiOWViYWE5MTRkMjY3OWUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYTA5OGZlNjZjNjk3MTg3MDFlM2M2ZTQ2MmYzNjY5YzA5NjViOWFkIn0=','2019-07-23 11:40:42.353826'),('am3giwzcikijxmz2r128tg5jim4n550a','ZjFkMTA1MWQ1NDkyMTcyNjQ0ZDRkOGM4YjI0Y2IwZjYxYjIzY2Q2NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTM5MTc2OWMzMTk5ZjNkNDAyYzA5OWFjMzBmMjkzNThmNTNjMjMwIn0=','2019-07-14 11:05:07.200075'),('cpw6k8bobo3uno190zld0u5prqyarsg8','ZjFkMTA1MWQ1NDkyMTcyNjQ0ZDRkOGM4YjI0Y2IwZjYxYjIzY2Q2NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTM5MTc2OWMzMTk5ZjNkNDAyYzA5OWFjMzBmMjkzNThmNTNjMjMwIn0=','2019-06-14 07:50:18.462522'),('e1924tp1ad3i8x5wo6dw1c3xqnxbrar9','YmNjMDlhOTIxMTIzNjk4ZTAyOTA1NmZiOWViYWE5MTRkMjY3OWUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYTA5OGZlNjZjNjk3MTg3MDFlM2M2ZTQ2MmYzNjY5YzA5NjViOWFkIn0=','2019-06-13 15:50:13.529650'),('e1wyzg6j2nxmayoxraf2g5azie46jozt','ZjFkMTA1MWQ1NDkyMTcyNjQ0ZDRkOGM4YjI0Y2IwZjYxYjIzY2Q2NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTM5MTc2OWMzMTk5ZjNkNDAyYzA5OWFjMzBmMjkzNThmNTNjMjMwIn0=','2019-07-18 06:28:22.432348'),('ekwr7adsk8mpm8yx0ossbdekac38vsrw','ZjFkMTA1MWQ1NDkyMTcyNjQ0ZDRkOGM4YjI0Y2IwZjYxYjIzY2Q2NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTM5MTc2OWMzMTk5ZjNkNDAyYzA5OWFjMzBmMjkzNThmNTNjMjMwIn0=','2019-07-02 12:51:39.284705'),('g0pll0igaxheqhg5nx9e3yeptnb1433j','YmNjMDlhOTIxMTIzNjk4ZTAyOTA1NmZiOWViYWE5MTRkMjY3OWUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYTA5OGZlNjZjNjk3MTg3MDFlM2M2ZTQ2MmYzNjY5YzA5NjViOWFkIn0=','2019-06-27 11:48:29.716943'),('gf6ulugqtn1gwlpx8u1i9ixztc24zzhq','YmNjMDlhOTIxMTIzNjk4ZTAyOTA1NmZiOWViYWE5MTRkMjY3OWUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYTA5OGZlNjZjNjk3MTg3MDFlM2M2ZTQ2MmYzNjY5YzA5NjViOWFkIn0=','2019-07-18 14:56:08.084147'),('h38ztjt4vwr3urc84j3rpxkpxhtaw67x','ZjFkMTA1MWQ1NDkyMTcyNjQ0ZDRkOGM4YjI0Y2IwZjYxYjIzY2Q2NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTM5MTc2OWMzMTk5ZjNkNDAyYzA5OWFjMzBmMjkzNThmNTNjMjMwIn0=','2019-06-12 10:42:21.793360'),('hlhoybjdbitdezkgsi4gcjl53cj761sc','ZjFkMTA1MWQ1NDkyMTcyNjQ0ZDRkOGM4YjI0Y2IwZjYxYjIzY2Q2NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTM5MTc2OWMzMTk5ZjNkNDAyYzA5OWFjMzBmMjkzNThmNTNjMjMwIn0=','2019-07-14 10:59:15.966860'),('i74tp6zzbqgawo6hbm61nijw7bksj9je','YmNjMDlhOTIxMTIzNjk4ZTAyOTA1NmZiOWViYWE5MTRkMjY3OWUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYTA5OGZlNjZjNjk3MTg3MDFlM2M2ZTQ2MmYzNjY5YzA5NjViOWFkIn0=','2019-06-27 12:14:20.431416'),('k39yxibxsqrt4o4s7v6mqit0bnfqwwz8','YmNjMDlhOTIxMTIzNjk4ZTAyOTA1NmZiOWViYWE5MTRkMjY3OWUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYTA5OGZlNjZjNjk3MTg3MDFlM2M2ZTQ2MmYzNjY5YzA5NjViOWFkIn0=','2019-07-06 15:26:38.881119'),('u0pwyrxx3fzkibsf78owjmy7um70nvg5','YmNjMDlhOTIxMTIzNjk4ZTAyOTA1NmZiOWViYWE5MTRkMjY3OWUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYTA5OGZlNjZjNjk3MTg3MDFlM2M2ZTQ2MmYzNjY5YzA5NjViOWFkIn0=','2019-06-12 17:37:13.692937'),('v8atvq95clth8e46mzhz9wif6r01nubs','ZjFkMTA1MWQ1NDkyMTcyNjQ0ZDRkOGM4YjI0Y2IwZjYxYjIzY2Q2NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTM5MTc2OWMzMTk5ZjNkNDAyYzA5OWFjMzBmMjkzNThmNTNjMjMwIn0=','2019-06-12 12:06:26.512848'),('xla9gbhee3bgau6yxhov5u1f79kq1dyq','ZjFkMTA1MWQ1NDkyMTcyNjQ0ZDRkOGM4YjI0Y2IwZjYxYjIzY2Q2NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTM5MTc2OWMzMTk5ZjNkNDAyYzA5OWFjMzBmMjkzNThmNTNjMjMwIn0=','2019-06-18 00:03:03.129892'),('xnavlhbqcpf4em2mfortsv5sk9n39lty','YmNjMDlhOTIxMTIzNjk4ZTAyOTA1NmZiOWViYWE5MTRkMjY3OWUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYTA5OGZlNjZjNjk3MTg3MDFlM2M2ZTQ2MmYzNjY5YzA5NjViOWFkIn0=','2019-06-20 08:16:10.147213'),('z3d03xfnsnrufun8o3toaicgjcu3joj2','YmNjMDlhOTIxMTIzNjk4ZTAyOTA1NmZiOWViYWE5MTRkMjY3OWUwODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjYTA5OGZlNjZjNjk3MTg3MDFlM2M2ZTQ2MmYzNjY5YzA5NjViOWFkIn0=','2019-06-13 15:45:09.644526'),('zg8oe69ngxj1cttog322uj9aq9osu2wh','ZjFkMTA1MWQ1NDkyMTcyNjQ0ZDRkOGM4YjI0Y2IwZjYxYjIzY2Q2NTp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJlYTM5MTc2OWMzMTk5ZjNkNDAyYzA5OWFjMzBmMjkzNThmNTNjMjMwIn0=','2019-06-17 14:16:52.807713');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-24  9:45:16
