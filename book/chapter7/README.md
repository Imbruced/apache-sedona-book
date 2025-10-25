# Chapter 7: Geospatial Data Science and Machine Learning

This chapter primary focus is on the integrating Apache Sedona with your machine learning
data workflows. You can achieve that by using the built in Sedona functionalities like:
- DBSCAN clustering
- Local Outlier Factor (LOF) for anomaly detection
- Local Getis–-Ord Gi(*) (Hotspot Analysis)
- Autocorrelation (Moran's I)
And also by integrating Sedona with popular machine learning libraries like:
- Apache Spark MLlib
- PyTorch

Each Subchapter contains a notebook with examples
- 1: Geospatial Clustering with Apache Sedona (DBSCAN) <b>ClusteringWithApacheSedona.ipynb</b>
- 2: Outlier Detection (Local Outlier Factor (LOF)) <b>OutlierDetection.ipynb</b>
- 3: Hot Spot Analysis (Local Getis–Ord Gi(*)) <b>HotspotAnalysis.ipynb</b>
- 4: Autocorrelation (Moran's I) <b>AutoCorrelation.ipynb</b>
- 5: Classification, Segmentation, and Object Detection from a Raster <b>RasterSegmentation.ipynb</b>
- 6: Creating Geospatial Machine Learning Models with MLlib <b>MLLib.ipynb</b>
- 7: Hands-On Use Case: Analyzing the road Accidents in Germany <b>AccidentAnalysis.ipynb</b>


To run examples using the docker compose

```bash
docker compose --profile chapter-7-1 up --build
```

then navigate to http://localhost:8888 in your browser and open the notebook

To run examples using the CLI

```bash
sedona provision --chapter chapter7 --sub-chapter 1 
```

The jupyter notebook will be automatically opened in your default browser.

For chapter 7-6 (MLLib.ipynb) it might take some time until the ors build the nodes, when the following curl command returns a valid response, you can open the notebook.

when it's ready the health check 
```bash
curl --location --request GET 'localhost:8085/ors/v2/health' \
--header 'Content-Type: application/json'
```

will return
```json
{"status":"ready"}
```

and the following curl command will return a valid response

```bash
curl --location 'localhost:8085/ors/v2/isochrones/foot-walking' \
--header 'Content-Type: application/json' \
--data '{
    "locations": [[2.319490, 48.868349]],
    "range": [600],
    "range_type": "time"
}'
```

will have a valid response
```
{
    "type": "FeatureCollection",
    "metadata": {
        "attribution": "openrouteservice.org, OpenStreetMap contributors",
        "service": "isochrones",
        "timestamp": 1761256875434,
        "query": ...,
    },
    "bbox": ...,
    "features": [
        {
            "type": "Feature",
            "properties": ...,
            "geometry": {
                "coordinates": [
                    [
                        [
                            2.310891,
                            48.872594
                        ]
                      ...
             
                    ]
                ],
                "type": "Polygon"
            }
        }
    ]
}
```

the invalid message might look as follows:

```json
{
  "error": {
    "message": "Cannot invoke \"org.heigit.ors.routing.RoutingProfile.getGraphhopper()\" because the return value of \"org.heigit.ors.routing.RoutingProfilesCollection.getRouteProfile(int)\" is null"
  },
  "info": {
    "engine": {
      "build_date": "2024-03-21T14:04:52Z",
      "version": "8.0.0"
    },
    "timestamp": 1761256472079
  }
}
```

if still after some period of time the response is invalid, you can restart the ors service in the docker compose setup.
before that make sure that you also clean the directory `/book/chapter7/ors` 
```bash
docker compose down --remove-orphans
docker compose --profile chapter-7-6 up --build
```