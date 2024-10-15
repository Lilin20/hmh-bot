DROP DATABASE hmh;
CREATE DATABASE hmh;

USE hmh;

CREATE TABLE users(
    discord_id      BIGINT PRIMARY KEY,
    name            VARCHAR(255),
    level           INT NOT NULL,
    xp              INT NOT NULL,
    growth          FLOAT NOT NULL,
    messages        INT NOT NULL,
    warns           INT NOT NULL,
    status          VARCHAR(255) NOT NULL DEFAULT("No status set... :(")
);

CREATE TABLE char_inventory(
    discord_id      BIGINT,
    char_name       VARCHAR(255),
    char_anime_eng  VARCHAR(255),
    char_anime_rom  VARCHAR(255),
    image_url       VARCHAR(255),
    collection_id   INT,
    FOREIGN KEY(discord_id) REFERENCES users(discord_id)
);

CREATE TABLE economy (
    user_id         BIGINT,
    balance         INT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(discord_id) ON DELETE CASCADE
);