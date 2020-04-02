CREATE SCHEMA IF NOT EXISTS `gamePlay` default character set utf8;
USE `gamePlay`;


CREATE TABLE IF NOT EXISTS `gamePlay`.`player` (
	`playerID` INT NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `gender` VARCHAR(255) NOT NULL,
    CONSTRAINT player_pk PRIMARY KEY (`playerID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`reviewer` (
	`reviewerID` INT NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `website` VARCHAR(255) NOT NULL,
    CONSTRAINT reviewer_pk PRIMARY KEY (`reviewerID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`publisher` (
	`publisherID` INT NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `location` VARCHAR(255) NOT NULL,
    CONSTRAINT publisher_pk PRIMARY KEY (`publisherID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`developer` (
	`developerID` INT NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `location` VARCHAR(255) NOT NULL,
    CONSTRAINT developer_pk PRIMARY KEY (`developerID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`platform` (
	`platformID` INT NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    CONSTRAINT platform_pk PRIMARY KEY (`platformID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`game` (
	`gameID` INT NOT NULL,
    `title` VARCHAR(45) NOT NULL,
    `description` VARCHAR(255) NOT NULL,
	`developerID` INT NOT NULL,
	`publisherID` INT NOT NULL,
	`ageRating` INT NOT NULL,
    `gameplayGenre` VARCHAR(45) NOT NULL,
	`aestheticGenre` VARCHAR(45) NOT NULL,
	`localPlayer` VARCHAR(45),
	`onlinePlayer` VARCHAR(45),
	`has_multiplayer` VARCHAR(45) NOT NULL,
	`has_campaign` VARCHAR(45) NOT NULL,
	`completionTime` TIME,
    CONSTRAINT game_pk PRIMARY KEY (`gameID`),
	CONSTRAINT game_fk1 FOREIGN KEY (`developerID`) 
		references developer(`developerID`) 
        ON UPDATE CASCADE ON DELETE CASCADE,
	CONSTRAINT game_fk2 FOREIGN KEY (`publisherID`) 
		references publisher(`publisherID`) 
        ON UPDATE CASCADE ON DELETE CASCADE)
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`player_game` (
	`playerID` INT NOT NULL,
	`gameID` INT NOT NULL,
	`playtime` INT,
    CONSTRAINT playergame_pk PRIMARY KEY (`playerID`, `gameID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`reviewer_game` (
	`reviewerID` INT NOT NULL,
	`gameID` INT NOT NULL,
	`reviewScore` INT NOT NULL,
    CONSTRAINT reviewergame_pk PRIMARY KEY (`reviewerID`, `gameID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`platform_game` (
	`platformID` INT NOT NULL,
	`gameID` INT NOT NULL,
    CONSTRAINT platformgame_pk PRIMARY KEY (`platformID`, `gameID`))
;