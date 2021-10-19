CREATE DATABASE IF NOT EXISTS test;
use test;

CREATE TABLE users (
    user_id INT(8) NOT NULL,
    password VARCHAR(270) NOT  NULL,
    email varchar(30) unique,
    youtube_api_key VARCHAR(270) NOT NULL,
    last_watched_video_id VARCHAR(30) NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE users
  ADD PRIMARY KEY (user_id);

ALTER TABLE users
  MODIFY user_id int(8) AUTO_INCREMENT,AUTO_INCREMENT=1;

INSERT INTO users (password, email, youtube_api_key, last_watched_video_id)
        VALUES ("5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
                "example@gmail.com",
                "AIzaSyDKY9T6Z7XYPRlCx6fLdfeujLfmPnDkldk",
                "BN9yqF6Um98");

CREATE TABLE toeic_info (
    user_id INT(8) NOT NULL,
    toeic_score INT(3) NULL,
    toeic_level INT(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE toeic_info
  ADD PRIMARY KEY (user_id);

INSERT INTO toeic_info (user_id, toeic_score, toeic_level)
        VALUES(1, 600 , 6);


CREATE TABLE words (
  user_id Int(8) NOT NULL,
  video_id varchar(30),
  english varchar(30) NOT NULL,
  japanese varchar(200) NOT NULL,
  watched_day date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO words (user_id, video_id, english, japanese, watched_day)
        VALUES(1, "BN9yqF6Um98", "english", "英語", '2020-05-01')




        


