-- create the Twitter database
CREATE DATABASE IF NOT EXISTS twitter_db;
USE twitter_db;

-- drop tables if they exist
DROP TABLE IF EXISTS tweet;
DROP TABLE IF EXISTS follows;

-- create TWEET table
CREATE TABLE tweet (
    tweet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    tweet_ts DATETIME NOT NULL,
    tweet_text VARCHAR(140) NOT NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_tweet_ts (tweet_ts),
    INDEX idx_user_ts (user_id, tweet_ts)
) ENGINE=InnoDB;

-- create FOLLOWS table
CREATE TABLE follows (
    follower_id INT NOT NULL,
    followee_id INT NOT NULL,
    PRIMARY KEY (follower_id, followee_id),
    INDEX idx_follower (follower_id),
    INDEX idx_followee (followee_id)
) ENGINE=InnoDB;

SHOW TABLES;
