CREATE DATABASE IF NOT EXISTS sample_demo_db;
use sample_demo_db;

CREATE TABLE `movie` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `popularity` varchar(4) NOT NULL,
  `director` varchar(250) NOT NULL,
  `imdb_score` varchar(4) NOT NULL,
  `name` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `genre` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `movie_genre` (
  `movie_id` int unsigned NOT NULL,
  `genre_id` int unsigned NOT NULL,
  FOREIGN KEY (`movie_id`) REFERENCES movie(id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (`genre_id`) REFERENCES genre(id) ON DELETE RESTRICT ON UPDATE CASCADE,
  PRIMARY KEY (`movie_id`, `genre_id`),
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

