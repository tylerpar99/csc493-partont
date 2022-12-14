DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(120) TEXT UNIQUE NOT NULL,
  firstName VARCHAR(120) NOT NULL,
  lastName VARCHAR(120) NOT NULL,
  email VARCHAR(120) TEXT UNIQUE NOT NULL,
  password VARCHAR(120) NOT NULL
);
