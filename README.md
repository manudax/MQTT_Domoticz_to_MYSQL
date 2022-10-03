# MQTT_Domoticz_to_MYSQL
Convert a MQTT frame from sensors or Domoticz to a MYSQL database

Create database :

CREATE DATABASE IF NOT EXISTS `database`
USE `database`;
CREATE TABLE IF NOT EXISTS `sensors` (
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idx` int(11) NOT NULL,
  `nvalue` int(11) DEFAULT NULL,
  `svalue` tinytext DEFAULT NULL,
  `nbr` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22895 DEFAULT CHARSET=utf8mb4;
