CREATE SCHEMA IF NOT EXISTS `gamePlay` default character set utf8;
USE `gamePlay`;

CREATE TABLE IF NOT EXISTS `gamePlay`.`player` (
	`id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(45) UNIQUE NOT NULL,
    `gender` VARCHAR(45) NOT NULL,
    `playtime` INT,
    CONSTRAINT player_pk PRIMARY KEY (`id`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`reviewer` (
	`reviewerID` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(45) NOT NULL,
    `website` VARCHAR(255) NOT NULL,
    CONSTRAINT reviewer_pk PRIMARY KEY (`reviewerID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`location` (
	`locationIndex` INT NOT NULL AUTO_INCREMENT,
    `city` VARCHAR(45) NOT NULL,
    `state/province` VARCHAR(45),
    `country` VARCHAR(45) NOT NULL,
    CONSTRAINT player_pk PRIMARY KEY (`locationIndex`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`publisher` (
	`publisherID` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(45) NOT NULL,
	`locationIndex` INT NOT NULL,
    CONSTRAINT publisher_pk PRIMARY KEY (`publisherID`),
	CONSTRAINT publisher_fk FOREIGN KEY (`locationIndex`) 
		references location(`locationIndex`) 
        ON UPDATE CASCADE ON DELETE CASCADE)
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`developer` (
	`developerID` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(45) NOT NULL,
	`locationIndex` INT NOT NULL,
    CONSTRAINT developer_pk PRIMARY KEY (`developerID`),
	CONSTRAINT developer_fk FOREIGN KEY (`locationIndex`) 
		references location(`locationIndex`) 
        ON UPDATE CASCADE ON DELETE CASCADE)
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`platform` (
	`platformID` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(45) NOT NULL,
    CONSTRAINT platform_pk PRIMARY KEY (`platformID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`gameplayGenre` (
	`gGenreID` INT NOT NULL AUTO_INCREMENT,
	`gGenreTitle` VARCHAR(45) NOT NULL,
	CONSTRAINT game_genre_pk PRIMARY KEY (`gGenreID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`aestheticGenre` (
	`aGenreID` INT NOT NULL AUTO_INCREMENT,
	`aGenreTitle` VARCHAR(45) NOT NULL,
	CONSTRAINT game_genre_pk PRIMARY KEY (`aGenreID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`game` (
	`gameID` INT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(45) NOT NULL,
    `description` VARCHAR(255) NOT NULL,
	`developerID` INT NOT NULL,
	`publisherID` INT NOT NULL,
	`ageRating` VARCHAR(45) NOT NULL,
    `gameplayGenre` INT NOT NULL,
	`aestheticGenre` INT NOT NULL,
	`localPlayer` INT,
	`onlinePlayer` INT,
	`has_multiplayer` VARCHAR(45) NOT NULL,
	`has_campaign` VARCHAR(45) NOT NULL,
	`completionTime` INT,
	`reviewScore` INT,
    CONSTRAINT game_pk PRIMARY KEY (`gameID`),
	CONSTRAINT game_fk1 FOREIGN KEY (`developerID`) 
		references developer(`developerID`) 
        ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT game_fk2 FOREIGN KEY (`publisherID`) 
		references publisher(`publisherID`) 
        ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT game_fk3 FOREIGN KEY (`gameplayGenre`) 
		references gameplayGenre(`gGenreID`) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT game_fk4 FOREIGN KEY (`aestheticGenre`) 
		references aestheticGenre(`aGenreID`) 
        ON UPDATE CASCADE ON DELETE CASCADE)
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`player_game` (
	`playerId` INT NOT NULL,
	`gameID` INT NOT NULL,
	`playtime` INT,
    CONSTRAINT playergame_pk PRIMARY KEY (`playerId`, `gameID`),
	CONSTRAINT game_player_fk1 FOREIGN KEY (`playerId`) 
		references player(`id`) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT game_player_fk2 FOREIGN KEY (`gameID`) 
		references game(`gameID`) 
        ON UPDATE CASCADE ON DELETE CASCADE)
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`reviewer_game` (
	`reviewerID` INT NOT NULL,
	`gameID` INT NOT NULL,
	`reviewScore` INT NOT NULL,
	`url` VARCHAR(100),
    CONSTRAINT reviewergame_pk PRIMARY KEY (`reviewerID`, `gameID`),
	CONSTRAINT game_review_fk1 FOREIGN KEY (`reviewerID`) 
			references reviewer(`reviewerID`) 
	        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT game_review_fk2 FOREIGN KEY (`gameID`) 
		references game(`gameID`) 
        ON UPDATE CASCADE ON DELETE CASCADE)
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`platform_game` (
	`platformID` INT NOT NULL,
	`gameID` INT NOT NULL,
    CONSTRAINT platformgame_pk PRIMARY KEY (`platformID`, `gameID`),
	CONSTRAINT game_platform_fk1 FOREIGN KEY (`platformID`) 
		references platform(`platformID`) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT game_platform_fk2 FOREIGN KEY (`gameID`) 
		references game(`gameID`) 
        ON UPDATE CASCADE ON DELETE CASCADE)
;
DROP PROCEDURE IF EXISTS add_game_to_database;
DELIMITER //
CREATE PROCEDURE add_game_to_database(
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
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS get_users_games;
DELIMITER //
CREATE PROCEDURE get_users_games(
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
    
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS remove_game_from_collection;
DELIMITER //
CREATE PROCEDURE remove_game_from_collection(
	IN gameId INT,
    IN playerId INT
)
BEGIN
	DELETE FROM player_game WHERE
		player_game.gameID = gameId
	AND
		player_game.playerId = playerId;
		
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS delete_user;
DELIMITER //
CREATE PROCEDURE delete_user(
	IN username VARCHAR(45)
)
BEGIN
	DECLARE uID INT;
    SELECT id INTO uID FROM player WHERE name = username;
    DELETE FROM player_game WHERE
		playerId = uID;
	DELETE FROM player WHERE id = uID;
END//
DELIMITER ;

DROP TRIGGER IF EXISTS insert_reveiw;
DELIMITER //
CREATE TRIGGER insert_reveiw
AFTER INSERT
ON reviewer_game FOR EACH ROW
BEGIN
	UPDATE game SET game.reviewScore = (SELECT AVG(reviewScore) FROM reviewer_game WHERE gameID = NEW.gameID) WHERE NEW.gameID = game.gameID;
END//
DELIMITER ;

DROP TRIGGER IF EXISTS update_playtime;
DELIMITER //
CREATE TRIGGER update_playtime
AFTER UPDATE
ON player_game FOR EACH ROW
BEGIN
	UPDATE player SET player.playtime = (SELECT SUM(playtime) FROM player_game WHERE playerId = NEW.playerId) WHERE player.id = NEW.playerId;
END//
DELIMITER ;