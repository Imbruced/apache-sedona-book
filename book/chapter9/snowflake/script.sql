-- create database
CREATE DATABASE SEDONA;

USE DATABASE SEDONA;

-- create stage
CREATE STAGE APACHESEDONA
	DIRECTORY = ( ENABLE = true );

-- download Sedona jar files
    -- https://mvnrepository.com/artifact/org.apache.sedona/sedona-snowflake/1.7.2
    -- For example using the command below
        -- wget https://repo1.maven.org/maven2/org/apache/sedona/sedona-snowflake/1.7.2/sedona-snowflake-1.7.2.jar
    -- https://mvnrepository.com/artifact/org.datasyslab/geotools-wrapper/1.7.2-28.5
    -- For example using the command below
        -- https://repo1.maven.org/maven2/org/datasyslab/geotools-wrapper/1.7.2-28.5/geotools-wrapper-1.7.2-28.5.jar

-- create schema
CREATE SCHEMA SEDONA;

-- create sedona SQL script to create functions
-- java -jar sedona-snowflake-1.7.2.jar --geotools-version 1.7.2-28.5 > sedona-snowflake.sql

-- create worksheet and run SQL script created above

-- create Sedona Geometry object from WKT
SELECT SEDONA.ST_GeomFromText('POINT(45.811357 6.967252)') AS geom

-- create snowflake geometry from Sedona Geometry object
CREATE TABLE point AS SELECT SEDONA.ST_GeomFromText('POINT(45.811357 6.967252)') as geom;

SELECT to_geometry(geom) FROM point;

-- create snowflake geography from Sedona Geometry object
SELECT to_geography(geom) FROM point;

-- convert snowflake geometry to Sedona Geometry object
CREATE TABLE snowflake_point AS
SELECT to_geometry(geom) AS geom FROM point;

SELECT ST_AsEWKB(geom) AS geom FROM snowflake_point;

SELECT SEDONA.ST_X(ST_AsEWKB(geom)) AS area FROM snowflake_point;

-- working with SRIDs
CREATE TABLE point_srid AS
SELECT SEDONA.ST_GeomFromText(
    'POINT(-122.116188 37.507550)',
    4326
) as geom;

-- preserving SRID
SELECT
    SEDONA.ST_SRID(SEDONA.ST_Buffer(SEDONA.ST_TRANSFORM(geom, 'epsg:4326', 'epsg:3857'), 250))
FROM point_srid


-- loosing SRID
SELECT
    SEDONA.ST_SRID(
            ST_GeomFromText('POINT(45.811357 6.967252)', 4326)
    ) AS geom

-- preserving SRID
SELECT SEDONA.ST_SRID(
    ST_ASEWKB(
        ST_GeomFromText('POINT(45.811357 6.967252)', 4326)
    )
) AS geom


-- USING GEOJSON based UDF functions provided by Apache Sedona
SELECT SEDONA.ST_DumpPoints(ST_GeomFromText('LINESTRING (0 0, 1 1, 1 0)'))


-- user defined table functions

WITH PLACES AS (
SELECT
    sedona.ST_GeomFromText('POINT (37.356569 -3.070110)') AS geom,
    'Africa' AS continent
UNION
SELECT
    sedona.ST_GeomFromText('POINT (25.853491 -17.924335)') AS geom,
    'Africa' AS continent
UNION
SELECT
    sedona.ST_GeomFromText('POINT (78.042126 27.174978)') AS geom,
    'Asia' AS continent
)
SELECT sedona.ST_AsText(collection) AS geom, continent
FROM PLACES,
    TABLE(sedona.ST_Collect(PLACES.geom) OVER (PARTITION BY continent));