DROP DATABASE IF EXISTS temperature_db;
CREATE DATABASE temperature_db;

\c socialdata;   

CREATE TABLE temperature (
    id SERIAL PRIMARY KEY,
    region VARCHAR(100),
    country VARCHAR(200),
    city VARCHAR(150),
    dt Date
    avg_temperature NUMERIC(8, 2),
);

