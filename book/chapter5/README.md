# Chapter 5: Raster Data Analysis
In this chapter we explore how to work with raster datatype using Apache Sedona.

We will cover the following topics:
- The Raster Data Model, how the raster is built, what is affine transformation and it's components
- Raster SQL and raster data manipulation, including:
  - loading and creating raster data
  - writing to raster formats
  - pixel functions
  - raster geometry functions, so for instance how to get raster extent
  - raster accessors, which return the raster parameters, like Height or affine transformation properties such as scalex or skewy
  - raster band accessors, like statistics or zonal statistics
  - raster predicates
  - raster based operators, like raster clipping
  - raster reshaping using tiles functions
  - raster visualisation functions
- Zonal Statistics with Apache Sedona
- Map Algebra with Apache Sedona
- Joining Raster data with Raster or Geometry data
- Hands-On Use Case: Insurance Risk Modeling

Each Subchapter contains a notebook with examples

1: The Raster Data Model <b>RasterModel.ipynb</b>

2: Raster SQL and Raster Data Manipulation <b>Raster SQL and Raster Data Manipulation.ipynb</b>

3: Zonal Statistics <b>Zonal Statistics.ipynb</b>

4: Map Algebra <b>MapAlgebra.ipynb</b>

5: Joining Raster Data </b>RasterJoin.ipynb</b>

6: Hands-On Use Case: Insurance Risk Modeling <b>Use Case Insurance Risk Modeling.ipynb</b>

To run examples using the docker compose

```bash
docker compose --profile chapter-5-1 up --build
```

then navigate to http://localhost:8888 in your browser and open the notebook

