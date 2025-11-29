#!/bin/bash
set -e

SEDONA_VERSION=1.8.0
SPARK_VERSION=3.5
SCALA_VERSION=2.12
GEOTOOLS_VERSION=33.1

#Download jar files and put them in the Spark jars directory
sudo curl -o /usr/lib/spark/jars/sedona-spark-shaded-${SPARK_VERSION}_${SCALA_VERSION}-${SEDONA_VERSION}.jar "https://repo1.maven.org/maven2/org/apache/sedona/sedona-spark-shaded-${SPARK_VERSION}_${SCALA_VERSION}/${SEDONA_VERSION}/sedona-spark-shaded-${SPARK_VERSION}_${SCALA_VERSION}-${SEDONA_VERSION}.jar"

sudo curl -o /usr/lib/spark/jars/geotools-wrapper-${SEDONA_VERSION}-${GEOTOOLS_VERSION}.jar "https://repo1.maven.org/maven2/org/datasyslab/geotools-wrapper/${SEDONA_VERSION}-${GEOTOOLS_VERSION}/geotools-wrapper-${SEDONA_VERSION}-${GEOTOOLS_VERSION}.jar"

#Install necessary python libraries
apt-get -y update

/opt/conda/miniconda3/bin/python -m pip install apache-sedona==${SEDONA_VERSION}
