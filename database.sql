CREATE SCHEMA IF NOT EXISTS `gamePlay` default character set utf8;
USE `gamePlay`;


CREATE TABLE IF NOT EXISTS `gamePlay`.`player` (
	`playerID` INT NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    `gender` VARCHAR(45) NOT NULL,
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
    `city` VARCHAR(45) NOT NULL,
    `country` VARCHAR(45) NOT NULL,
    CONSTRAINT publisher_pk PRIMARY KEY (`publisherID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`location` (
	`locationIndex` INT NOT NULL,
    `City` VARCHAR(45) NOT NULL,
    `Country` VARCHAR(45) NOT NULL,
    CONSTRAINT player_pk PRIMARY KEY (`locationIndex`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`developer` (
	`developerID` INT NOT NULL,
    `name` VARCHAR(45) NOT NULL,
	`locationIndex` INT NOT NULL,
    CONSTRAINT developer_pk PRIMARY KEY (`developerID`),
	CONSTRAINT developer_fk FOREIGN KEY (`locationIndex`) 
		references location(`locationIndex`) 
        ON UPDATE CASCADE ON DELETE CASCADE)
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`platform` (
	`platformID` INT NOT NULL,
    `name` VARCHAR(45) NOT NULL,
    CONSTRAINT platform_pk PRIMARY KEY (`platformID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`gameplayGenre` (
	`gGenreID` INT NOT NULL,
	`gGenreTitle` VARCHAR(45) NOT NULL,
	CONSTRAINT game_genre_pk PRIMARY KEY (`gGenreID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`aestheticGenre` (
	`aGenreID` INT NOT NULL,
	`aGenreTitle` VARCHAR(45) NOT NULL,
	CONSTRAINT game_genre_pk PRIMARY KEY (`aGenreID`))
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`game` (
	`gameID` INT NOT NULL,
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
	`playerID` INT NOT NULL,
	`gameID` INT NOT NULL,
	`playtime` INT,
    CONSTRAINT playergame_pk PRIMARY KEY (`playerID`, `gameID`),
	CONSTRAINT game_player_fk1 FOREIGN KEY (`playerID`) 
		references player(`playerID`) 
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT game_player_fk2 FOREIGN KEY (`gameID`) 
		references game(`gameID`) 
        ON UPDATE CASCADE ON DELETE CASCADE)
;

CREATE TABLE IF NOT EXISTS `gamePlay`.`reviewer_game` (
	`reviewerID` INT NOT NULL,
	`gameID` INT NOT NULL,
	`reviewScore` INT NOT NULL,
	`url` VARCHAR(100) NOT NULL,
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
