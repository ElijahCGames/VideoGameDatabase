CREATE DATABASE  IF NOT EXISTS `gamePlay` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `gamePlay`;
-- MySQL dump 10.13  Distrib 8.0.19, for macos10.15 (x86_64)
--
-- Host: 127.0.0.1    Database: gamePlay
-- ------------------------------------------------------
-- Server version	8.0.19

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
-- Table structure for table `aestheticGenre`
--

DROP TABLE IF EXISTS `aestheticGenre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aestheticGenre` (
  `aGenreID` int NOT NULL AUTO_INCREMENT,
  `aGenreTitle` varchar(45) NOT NULL,
  PRIMARY KEY (`aGenreID`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aestheticGenre`
--

LOCK TABLES `aestheticGenre` WRITE;
/*!40000 ALTER TABLE `aestheticGenre` DISABLE KEYS */;
INSERT INTO `aestheticGenre` VALUES (1,'Realistic Fantasy'),(2,'Cartoony'),(3,'Realistic Modern'),(4,'Hand-Drawn'),(5,'Sci-Fi'),(6,'Steampunk'),(7,'Cyberpunk'),(8,'Historical'),(9,'Futuristic'),(10,'Dystopian'),(11,'Utopian'),(12,'Photorealistic'),(13,'Exaggerated'),(14,'Abstract'),(15,'Cel-Shaded'),(16,'Western'),(17,'Horror'),(18,'Mystery'),(19,'Crime/Detective'),(20,'Mythology'),(21,'Post-apocalyptic'),(22,'War');
/*!40000 ALTER TABLE `aestheticGenre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `developer`
--

DROP TABLE IF EXISTS `developer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `developer` (
  `developerID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `locationIndex` int NOT NULL,
  PRIMARY KEY (`developerID`),
  KEY `developer_fk` (`locationIndex`),
  CONSTRAINT `developer_fk` FOREIGN KEY (`locationIndex`) REFERENCES `location` (`locationIndex`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `developer`
--

LOCK TABLES `developer` WRITE;
/*!40000 ALTER TABLE `developer` DISABLE KEYS */;
INSERT INTO `developer` VALUES (1,'Nintedo EPD',2),(2,'P Studio',1),(3,'Square Enix',1),(4,'Matt Makes Games',9),(5,'Platinum Games',6),(6,'Infinity Ward',10),(7,'Yacht Club Games',10),(8,'Next Level Games',9),(9,'Moon Studios',12),(10,'SIE Santa Monica Studio',4),(11,'Naughty Dog',4),(12,'SIE Japan Studio',1),(13,'SIE Bend Studio',13),(14,'Guerrilla Games',14),(15,'Sucker Punch Productions',15),(16,'SIE San Diego Studio',16),(17,'Insomniac Games',17),(18,'SIE San Mateo Studio',18),(19,'SIE London Studio',19),(20,'Media Molecule',20),(21,'Pixelopus',18),(22,'Polyphony Digital',1),(23,'343 Industries',3),(24,'Compulsion Games',21),(25,'inXile Entertainment',22),(26,'Double Fine',23),(27,'Mojang',24),(28,'Ninja Theory',25),(29,'Obsidian Entertainment',11),(30,'Playground Games',26),(31,'Rare',27),(32,'The Coalition',9),(33,'The Initiative',18),(34,'Turn 10 Studios',8),(35,'Undead Labs',28),(36,'World\'s Edge',8),(37,'CD Projekt',29),(38,'Bethesda Game Studios',5),(39,'Rockstar Games',30),(40,'Gearbox Software',32),(41,'Arc System Works',1),(42,'Bungie',15);
/*!40000 ALTER TABLE `developer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `game` (
  `gameID` int NOT NULL AUTO_INCREMENT,
  `title` varchar(45) NOT NULL,
  `description` varchar(255) NOT NULL,
  `developerID` int NOT NULL,
  `publisherID` int NOT NULL,
  `ageRating` varchar(45) NOT NULL,
  `gameplayGenre` int NOT NULL,
  `aestheticGenre` int NOT NULL,
  `localPlayer` int DEFAULT NULL,
  `onlinePlayer` int DEFAULT NULL,
  `has_multiplayer` varchar(45) NOT NULL,
  `has_campaign` varchar(45) NOT NULL,
  `completionTime` int DEFAULT NULL,
  `reviewScore` int DEFAULT NULL,
  PRIMARY KEY (`gameID`),
  KEY `game_fk1` (`developerID`),
  KEY `game_fk2` (`publisherID`),
  KEY `game_fk3` (`gameplayGenre`),
  KEY `game_fk4` (`aestheticGenre`),
  CONSTRAINT `game_fk1` FOREIGN KEY (`developerID`) REFERENCES `developer` (`developerID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `game_fk2` FOREIGN KEY (`publisherID`) REFERENCES `publisher` (`publisherID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `game_fk3` FOREIGN KEY (`gameplayGenre`) REFERENCES `gameplayGenre` (`gGenreID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `game_fk4` FOREIGN KEY (`aestheticGenre`) REFERENCES `aestheticGenre` (`aGenreID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game`
--

LOCK TABLES `game` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;
INSERT INTO `game` VALUES (1,'Animal Crossing: New Horizons','',1,1,'E',2,2,8,8,'TRUE','TRUE',50,9),(2,'Persona 5','',2,2,'M',1,1,1,0,'FALSE','TRUE',80,10),(3,'Gears 5','',32,9,'M',3,5,3,10,'TRUE','TRUE',10,0),(4,'The Witcher 3: Wild Hunt','',37,14,'M',34,1,1,0,'FALSE','TRUE',51,0),(5,'Celeste','',4,12,'E10',5,14,1,0,'FALSE','TRUE',8,0);
/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gameplayGenre`
--

DROP TABLE IF EXISTS `gameplayGenre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gameplayGenre` (
  `gGenreID` int NOT NULL AUTO_INCREMENT,
  `gGenreTitle` varchar(45) NOT NULL,
  PRIMARY KEY (`gGenreID`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gameplayGenre`
--

LOCK TABLES `gameplayGenre` WRITE;
/*!40000 ALTER TABLE `gameplayGenre` DISABLE KEYS */;
INSERT INTO `gameplayGenre` VALUES (1,'JRPG'),(2,'Simulation'),(3,'Third-Person Shooter'),(4,'First-Person Shooter'),(5,'Platformer'),(6,'Turn-Based Strategy'),(7,'RPG'),(8,'RTS'),(9,'MMO'),(10,'MMORPG'),(11,'MOBA'),(12,'Fighting'),(13,'Beat \'em up'),(14,'Stealth'),(15,'Survival'),(16,'Battle Royale'),(17,'Rhythm'),(18,'Action-Adventure'),(19,'Survival Horror'),(20,'Metroidvania'),(21,'Visual Novel'),(22,'Action RPG'),(23,'Roguelike'),(24,'Tactical RPG'),(25,'Simulation'),(26,'4X'),(27,'Racing'),(28,'Sports'),(29,'Casual'),(30,'Board/Card Game'),(31,'CCG'),(32,'Party'),(33,'Puzzle'),(34,'Action');
/*!40000 ALTER TABLE `gameplayGenre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `location` (
  `locationIndex` int NOT NULL AUTO_INCREMENT,
  `city` varchar(45) NOT NULL,
  `state/province` varchar(45) DEFAULT NULL,
  `country` varchar(45) NOT NULL,
  PRIMARY KEY (`locationIndex`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` VALUES (1,'Tokyo','Kanto','Japan'),(2,'Kyoto','Kansai','Japan'),(3,'Redwood City','California','United States of America'),(4,'Santa Monica','California','United States of America'),(5,'Rockville','Maryland','United States of America'),(6,'Osaka','Kansai','Japan'),(7,'Montreuil','Ile-de-France','France'),(8,'Redmond','Washington','United States of America'),(9,'Vancouver','BC','Canada'),(10,'Los Angeles',' California','United States of America'),(11,'Irvine',' California','United States of America'),(12,'Vienna','','Austria'),(13,'Bend','Oregon','United States of America'),(14,'Amsterdam','North Holland','Netherlands'),(15,'Bellevue','Washington','United States of America'),(16,'San Diego','California','United States of America'),(17,'Burbank','California','United States of America'),(18,'San Mateo','California','United States of America'),(19,'London','','England'),(20,'Surrey','','England'),(21,'Montreal','Quebec','Canada'),(22,'Newport Beach','California','United States of America'),(23,'San Fransisco','California','United States of America'),(24,'Stockholm','','Sweden'),(25,'Cambridge','','England'),(26,'Leamington Spa','England',''),(27,'Twycross','','England'),(28,'Seattle','Washington','United States of America'),(29,'Warsaw','','Poland'),(30,'New York','New York','United States of America'),(31,'Novato','California','United States of America'),(32,'Frisco','Texas','United States of America'),(33,'Austin','Texas','United States of America'),(34,'Yokohama','Kanto','Japan'),(35,'Milan','','Italy'),(36,'Paris','Ile-de-France','France'),(37,'Hofen','','Austria');
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform`
--

DROP TABLE IF EXISTS `platform`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform` (
  `platformID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`platformID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform`
--

LOCK TABLES `platform` WRITE;
/*!40000 ALTER TABLE `platform` DISABLE KEYS */;
INSERT INTO `platform` VALUES (1,'PS4'),(2,'PS3'),(3,'Switch'),(4,'Xbox One'),(5,'Xbox 360'),(6,'PC');
/*!40000 ALTER TABLE `platform` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `platform_game`
--

DROP TABLE IF EXISTS `platform_game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `platform_game` (
  `platformID` int NOT NULL,
  `gameID` int NOT NULL,
  PRIMARY KEY (`platformID`,`gameID`),
  KEY `game_platform_fk2` (`gameID`),
  CONSTRAINT `game_platform_fk1` FOREIGN KEY (`platformID`) REFERENCES `platform` (`platformID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `game_platform_fk2` FOREIGN KEY (`gameID`) REFERENCES `game` (`gameID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `platform_game`
--

LOCK TABLES `platform_game` WRITE;
/*!40000 ALTER TABLE `platform_game` DISABLE KEYS */;
INSERT INTO `platform_game` VALUES (3,1),(1,2),(2,2),(4,3),(6,3),(1,4),(3,4),(4,4),(6,4),(1,5),(3,5),(4,5),(6,5);
/*!40000 ALTER TABLE `platform_game` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `player`
--

DROP TABLE IF EXISTS `player`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `gender` varchar(45) NOT NULL,
  `playtime` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player`
--

LOCK TABLES `player` WRITE;
/*!40000 ALTER TABLE `player` DISABLE KEYS */;
INSERT INTO `player` VALUES (1,'Elijah','Male',NULL),(2,'demo','None',7);
/*!40000 ALTER TABLE `player` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `player_game`
--

DROP TABLE IF EXISTS `player_game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `player_game` (
  `playerId` int NOT NULL,
  `gameID` int NOT NULL,
  `playtime` int DEFAULT NULL,
  PRIMARY KEY (`playerId`,`gameID`),
  KEY `game_player_fk2` (`gameID`),
  CONSTRAINT `game_player_fk1` FOREIGN KEY (`playerId`) REFERENCES `player` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `game_player_fk2` FOREIGN KEY (`gameID`) REFERENCES `game` (`gameID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `player_game`
--

LOCK TABLES `player_game` WRITE;
/*!40000 ALTER TABLE `player_game` DISABLE KEYS */;
INSERT INTO `player_game` VALUES (1,1,30),(1,2,2),(2,1,2),(2,2,5),(2,4,0);
/*!40000 ALTER TABLE `player_game` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `update_playtime` AFTER UPDATE ON `player_game` FOR EACH ROW BEGIN
	UPDATE player SET player.playtime = (SELECT SUM(playtime) FROM player_game WHERE playerId = NEW.playerId) WHERE player.id = NEW.playerId;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `publisher`
--

DROP TABLE IF EXISTS `publisher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `publisher` (
  `publisherID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `locationIndex` int NOT NULL,
  PRIMARY KEY (`publisherID`),
  KEY `publisher_fk` (`locationIndex`),
  CONSTRAINT `publisher_fk` FOREIGN KEY (`locationIndex`) REFERENCES `location` (`locationIndex`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `publisher`
--

LOCK TABLES `publisher` WRITE;
/*!40000 ALTER TABLE `publisher` DISABLE KEYS */;
INSERT INTO `publisher` VALUES (1,'Nintendo',2),(2,'Atlus',1),(3,'Ubisoft',7),(4,'Electronic Arts',3),(5,'Activision Blizzard',4),(6,'Bethesda Softworks',5),(7,'Platinum Games',6),(8,'Sony Interactive Entertainment (SIE)',1),(9,'Xbox Game Studios',8),(10,'Bandai Namco Entertainment',1),(11,'Square Enix',1),(12,'Matt Makes Games',9),(13,'Yacht Club Games',10),(14,'CD Projekt',29),(15,'Warner Bros. Interactive Entertainment',17),(16,'Rockstar Games',30),(17,'2K Games',31),(18,'Capcom',6),(19,'Paradox Interactive',24),(20,'SEGA',1),(21,'Devolver Digital',33),(22,'Konami',1),(23,'Koei Tecmo',34),(24,'505 Games',35),(25,'tinyBuild',15),(26,'Focus Home Interactive',36),(27,'Deep Silver',37),(28,'Arc System Works',1);
/*!40000 ALTER TABLE `publisher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviewer`
--

DROP TABLE IF EXISTS `reviewer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviewer` (
  `reviewerID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `website` varchar(255) NOT NULL,
  PRIMARY KEY (`reviewerID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviewer`
--

LOCK TABLES `reviewer` WRITE;
/*!40000 ALTER TABLE `reviewer` DISABLE KEYS */;
INSERT INTO `reviewer` VALUES (1,'IGN','https://www.ign.com/'),(2,'Gamespot','https://www.gamespot.com/'),(3,'Polygon','https://www.polygon.com/'),(4,'Kotaku','https://www.kotaku.com/');
/*!40000 ALTER TABLE `reviewer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviewer_game`
--

DROP TABLE IF EXISTS `reviewer_game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviewer_game` (
  `reviewerID` int NOT NULL,
  `gameID` int NOT NULL,
  `reviewScore` int NOT NULL,
  `url` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`reviewerID`,`gameID`),
  KEY `game_review_fk2` (`gameID`),
  CONSTRAINT `game_review_fk1` FOREIGN KEY (`reviewerID`) REFERENCES `reviewer` (`reviewerID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `game_review_fk2` FOREIGN KEY (`gameID`) REFERENCES `game` (`gameID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviewer_game`
--

LOCK TABLES `reviewer_game` WRITE;
/*!40000 ALTER TABLE `reviewer_game` DISABLE KEYS */;
INSERT INTO `reviewer_game` VALUES (1,1,9,'https://www.ign.com/articles/animal-crossing-new-horizons-review-for-switch'),(1,2,10,'https://en.wikipedia.org/wiki/Persona_5#cite_note-IGNreview-113');
/*!40000 ALTER TABLE `reviewer_game` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `insert_reveiw` AFTER INSERT ON `reviewer_game` FOR EACH ROW BEGIN
	UPDATE game SET game.reviewScore = (SELECT AVG(reviewScore) FROM reviewer_game WHERE gameID = NEW.gameID) WHERE NEW.gameID = game.gameID;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Dumping events for database 'gamePlay'
--

--
-- Dumping routines for database 'gamePlay'
--
/*!50003 DROP PROCEDURE IF EXISTS `add_game_to_database` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_game_to_database`(
	IN gameTitle VARCHAR(45),
    IN descript VARCHAR(255),
    IN devId INT,
    IN pubId INT,
    IN age VARCHAR(45),
    IN gID INT,
    IN aID INT,
    IN localM INT,
    IN onlineM INT,
    IN multi VARCHAR(45),
    IN camp VARCHAR(45),
    IN addToCollection BOOLEAN
)
BEGIN
	INSERT INTO game (title,`description`,developerID,publisherID,ageRating,gameplayGenre,aestheticGenre,localPlayer,onlinePlayer,has_multiplayer,has_campaign)
		VALUES (gameTitle,descript,devId,pubId,age,gID,aID,localM,onlineM,multi,camp);
	IF addToCollection THEN
		INSERT INTO player_game VALUES ((SELECT id FROM player WHERE name = @uname),(SELECT LAST_INSERT_ID()),0);
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `delete_user` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `delete_user`(
	IN username VARCHAR(45)
)
BEGIN
	DECLARE uID INT;
    SELECT id INTO uID FROM player WHERE name = username;
    DELETE FROM player_game WHERE
		playerId = uID;
	DELETE FROM player WHERE id = uID;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_users_games` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_users_games`(
	IN username VARCHAR(45)
)
BEGIN
	DECLARE UID INT;
    SELECT id INTO UID FROM player WHERE name = username;
    
	SELECT gameID, title, dev.name,pub.name 
    FROM game 
    INNER JOIN developer AS dev ON game.developerID = dev.developerID 
    INNER JOIN publisher AS pub ON pub.publisherID = game.publisherID
    WHERE gameID IN (SELECT gameID FROM player_game WHERE playerId = UID);
    
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `remove_game_from_collection` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `remove_game_from_collection`(
	IN gameId INT,
    IN playerId INT
)
BEGIN
	DELETE FROM player_game WHERE
		player_game.gameID = gameId
	AND
		player_game.playerId = playerId;
		
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-14 15:16:03
