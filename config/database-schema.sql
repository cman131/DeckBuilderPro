CREATE TABLE `Deck` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `description` varchar(250) DEFAULT NULL,
  `size` tinyint(250) unsigned DEFAULT NULL,
  `black` tinyint(250) DEFAULT 0,
  `blue` tinyint(250) DEFAULT 0,
  `green` tinyint(250) DEFAULT 0,
  `red` tinyint(250) DEFAULT 0,
  `white` tinyint(250) DEFAULT 0,
  `colorless` tinyint(250) DEFAULT 0,
  `publicity` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE TABLE `Deck_Card` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `deckid` bigint(20) NOT NULL,
  `cardid` varchar(30) NOT NULL,
  `count` tinyint(120) unsigned DEFAULT 1 NOT NULL,
  PRIMARY KEY (`id`)
 ) Engine=InnoDB DEFAULT CHARSET utf8;
CREATE TABLE `Card` (
  `id` varchar(100) NOT NULL,
  `name` varchar(250) DEFAULT NULL,
  `multiverseid` varchar(50) DEFAULT NULL,
  `manacost` varchar(250) DEFAULT NULL,
  `cmc` bigint(10) DEFAULT NULL,
  `colors` varchar(250) DEFAULT NULL,
  `types` varchar(250) DEFAULT NULL,
  `supertypes` varchar(250) DEFAULT NULL,
  `subtypes` varchar(250) DEFAULT NULL,
  `rarity` varchar(50) DEFAULT 'Common',
  `text` varchar(500) DEFAULT NULL,
  `flavor` varchar(250) DEFAULT NULL,
  `artist` varchar(250) DEFAULT NULL,
  `number` varchar(20) DEFAULT NULL,
  `power`  varchar(250) DEFAULT NULL,
  `toughness` varchar(250) DEFAULT NULL,
  `layout` varchar(250) DEFAULT 'normal',
  `imagename` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) Engine=InnoDB DEFAULT CHARSET utf8;
