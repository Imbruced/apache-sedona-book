CREATE EXTENSION POSTGIS;

CREATE TABLE points
(
    name     VARCHAR(50),
    location GEOMETRY
);

INSERT INTO points (name, location)
VALUES ('Point A',
        ST_GeomFromText('POINT(10.0 20.0)', 4326));

INSERT INTO points (name, location)
VALUES ('Point B',
        ST_GeomFromText('POINT(30.0 40.0)', 4326));

INSERT INTO points (name, location)
VALUES ('Point C',
        ST_GeomFromText('POINT(50.0 60.0)', 4326));

CREATE TABLE polygons
(
    name     VARCHAR(50),
    location GEOMETRY,
    created_at  TIMESTAMP,
    updated_at  TIMESTAMP
);

INSERT INTO polygons (name, location, created_at, updated_at)
VALUES ('Polygon A',
        ST_GeomFromText('POLYGON((10.0 20.0, 30.0 40.0, 50.0 60.0, 10.0 20.0))', 4326),
        '2024-01-01 12:36:00',
        null
);

INSERT INTO polygons (name, location, created_at, updated_at)
VALUES ('Polygon B',
        ST_GeomFromText('POLYGON((70.0 80.0, 90.0 100.0, 110.0 120.0, 70.0 80.0))', 4326),
        '2020-01-01 00:00:00',
        '2024-01-01 11:36:00');

INSERT INTO polygons (name, location, created_at, updated_at)
VALUES ('Polygon C',
        ST_GeomFromText('POLYGON((130.0 140.0, 150.0 160.0, 170.0 180.0, 130.0 140.0))', 4326),
        '2023-01-01 00:00:00',
        '2024-01-01 11:16:00');
