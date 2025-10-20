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