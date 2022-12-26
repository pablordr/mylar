CREATE DATABASE mylar;
\connect mylar postgres;
CREATE TABLE IF NOT EXISTS entries (
    id INT PRIMARY KEY,
    title VARCHAR(255));