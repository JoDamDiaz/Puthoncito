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

CREATE TABLE IF NOT EXISTS users (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    username         VARCHAR(50)  NOT NULL UNIQUE,
    email            VARCHAR(150) NOT NULL UNIQUE,
    hashed_password  VARCHAR(255) NOT NULL,
    is_active        BOOLEAN      NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
