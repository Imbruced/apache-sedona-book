CREATE TABLE points
(
    name     VARCHAR2(50),
    location SDO_GEOMETRY
);

INSERT INTO points (name, location)
VALUES ('Point A',
        SDO_GEOMETRY(2001, 4326, SDO_POINT_TYPE(10.0, 20.0, NULL), NULL, NULL));

INSERT INTO points (name, location)
VALUES ('Point B',
        SDO_GEOMETRY(2001, 4326, SDO_POINT_TYPE(30.0, 40.0, NULL), NULL, NULL));

INSERT INTO points (name, location)
VALUES ('Point C',
        SDO_GEOMETRY(2001, 4326, SDO_POINT_TYPE(50.0, 60.0, NULL), NULL, NULL));

COMMIT;

EXIT;