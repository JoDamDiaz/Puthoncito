CREATE DATABASE IF NOT EXISTS perritos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE perritos;

CREATE TABLE IF NOT EXISTS dogs (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(100)              NOT NULL,
    breed   VARCHAR(100)              NOT NULL,
    age     FLOAT                     NOT NULL,
    weight  FLOAT                     NOT NULL,
    sex     ENUM('macho', 'hembra')   NOT NULL,
    owner   VARCHAR(150)              NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS cats (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(100)              NOT NULL,
    breed   VARCHAR(100)              NOT NULL,
    age     FLOAT                     NOT NULL,
    weight  FLOAT                     NOT NULL,
    sex     ENUM('macho', 'hembra')   NOT NULL,
    owner   VARCHAR(150)              NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
