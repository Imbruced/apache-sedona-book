#!/bin/bash
SEDONA_VERSION=1.8.0
SPARK_VERSION=3.5
SCALA_VERSION=2.12
GEOTOOLS_VERSION=33.1

#EMR clusters only have ephemeral local storage. It does not really matter where we store the jars.
sudo mkdir /jars

#Download Sedona jar
sudo curl -o /jars/sedona-spark-shaded-${SPARK_VERSION}_${SCALA_VERSION}-${SEDONA_VERSION}.jar "https://repo1.maven.org/maven2/org/apache/sedona/sedona-spark-shaded-${SPARK_VERSION}_${SCALA_VERSION}/${SEDONA_VERSION}/sedona-spark-shaded-${SPARK_VERSION}_${SCALA_VERSION}-${SEDONA_VERSION}.jar"

#Download GeoTools jar
sudo curl -o /jars/geotools-wrapper-${SEDONA_VERSION}-${GEOTOOLS_VERSION}.jar "https://repo1.maven.org/maven2/org/datasyslab/geotools-wrapper/${SEDONA_VERSION}-${GEOTOOLS_VERSION}/geotools-wrapper-${SEDONA_VERSION}-${GEOTOOLS_VERSION}.jar"

#Install necessary python libraries
sudo python3 -m pip install pandas
sudo python3 -m pip install shapely
sudo python3 -m pip install geopandas
sudo python3 -m pip install keplergl==0.3.2
sudo python3 -m pip install pydeck==0.8.0
sudo python3 -m pip install attrs matplotlib descartes apache-sedona==${SEDONA_VERSION}

sudo alternatives --set java /usr/lib/jvm/java-11-amazon-corretto.x86_64/bin/java