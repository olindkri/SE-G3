DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS chat;
DROP TABLE IF EXISTS message;
DROP TABLE IF EXISTS guide_user;
DROP TABLE IF EXISTS images;

CREATE TABLE posts
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    byUser   INTEGER,
    created  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title    TEXT      NOT NULL,
    content  TEXT      NOT NULL,
    country  TEXT      NOT NULL,
    city     TEXT      NOT NULL,
    language TEXT,
    price    INTEGER   NOT NULL,
    FOREIGN KEY (byUser) REFERENCES user (id)
);

CREATE TABLE user
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT NOT NULL,
    lastname  TEXT NOT NULL,
    age       INTEGER,
    country   TEXT
);

CREATE TABLE chat
(
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    user1 INTEGER NOT NULL,
    user2 INTEGER NOT NULL,
    FOREIGN KEY (user1) REFERENCES user (id),
    FOREIGN KEY (user2) REFERENCES user (id)
);

CREATE TABLE message
(
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    date    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    inChat  INTEGER   NOT NULL,
    byUser  INTEGER   NOT NULL,
    FOREIGN KEY (byUser) REFERENCES user (id),
    FOREIGN KEY (inChat) REFERENCES chat (id)
);

CREATE TABLE guide_user
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user      INTEGER NOT NULL,
    guide     INTEGER NOT NULL,
    from_date DATE    NOT NULL,
    to_date   DATE    NOT NULL,
    FOREIGN KEY (user) REFERENCES user (id),
    FOREIGN KEY (guide) REFERENCES posts (id)
);

CREATE TABLE images
(
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    img  TEXT,
    user INTEGER NOT NULL,
    FOREIGN KEY (user) REFERENCES user (id)
);