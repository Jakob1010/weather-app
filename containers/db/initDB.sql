DROP DATABASE IF EXISTS temperature_db;
CREATE DATABASE temperature_db;

\c temperature_db;   
DROP TABLE IF EXISTS temperature;
DROP TABLE IF EXISTS measurement;

CREATE TABLE temperature (
    id SERIAL PRIMARY KEY,
    region VARCHAR(100),
    country VARCHAR(200),
    city VARCHAR(150),
    dt Date,
    celsius NUMERIC(8, 2),
    fahrenheit NUMERIC(8, 2)
);

CREATE TABLE measurement (
    id SERIAL PRIMARY KEY,
    region VARCHAR(100),
    country VARCHAR(200),
    city VARCHAR(150),
    accessed TIMESTAMP,
    temperature NUMERIC(8, 2)
);

