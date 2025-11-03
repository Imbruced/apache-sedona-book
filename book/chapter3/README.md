# Chapter 3: Loading Geospatial Data into Apache Sedona

In this chapter we will explore various methods to load data to the Apache Sedona
spatial data frame. We will show examples for loading:
- Vector data formats such as (Loading Vector Data Formats)
    - Shapefiles
    - GeoJSON
    - WKT
    - WKB
    - Geoparquet
    - OSM
    - GeoPackage
- Raster data formats such as (Introduction to Raster Data Formats (GeoTIFF))
    - GeoTIFF
- Data from spatial databases such as (Loading Data from Databases)
    - PostGIS
    - MongoDB
    - MySQL
    - From PostGIS using the Debezium

In the last part of this chapter we will analyze the NYC Taxi dataset using Apache Sedona
(Hands-On Use Case: New York Taxi Data Analysis).

Each section has it's own Notebook prepared with code, which you can interactively run
and modify. You can find the Notebooks in the `book/chapter3` folder.

Each Subchapter contains a notebook with examples
- 1: Loading Vector Data Formats <b>LoadingVectorDataFormats.ipynb</b>
- 2: Introduction to Raster Data Formats (GeoTIFF) <b>LoadingRasterData.ipynb</b>
- 3: Loading Data from Databases <b>ReadingFromPostgreSQL.ipynb</b>
- 4: Hands-On Use Case: New York Taxi Data Analysis <b>NewYorkTaxiAnalysis.ipynb</b>

You can run them using the docker-compose and the cli.

To run using docker-compose (chapter 3 sub chapter 1):

```bash
docker-compose --profile chapter3-1 up -d
```

