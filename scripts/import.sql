DROP DATABASE hmh;
CREATE DATABASE hmh;

USE hmh;

CREATE TABLE users(
    discord_id      BIGINT PRIMARY KEY,
    name            VARCHAR(255)
);

CREATE TABLE char_inventory(
    discord_id      BIGINT,
    char_name       VARCHAR(255),
    char_anime_eng  VARCHAR(255),
    char_anime_rom  VARCHAR(255)
);