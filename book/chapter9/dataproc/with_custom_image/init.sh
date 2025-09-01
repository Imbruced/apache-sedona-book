#!/bin/bash
set -e

#Download jar files and put them in the Spark jars directory
sudo curl -o /usr/lib/spark/jars/sedona-spark-shaded-3.5_2.12-1.7.0.jar "https://repo1.maven.org/maven2/org/apache/sedona/sedona-spark-shaded-3.5_2.12/1.7.0/sedona-spark-shaded-3.5_2.12-1.7.0.jar"

sudo curl -o /usr/lib/spark/jars/geotools-wrapper-1.7.0-28.5.jar "https://repo1.maven.org/maven2/org/datasyslab/geotools-wrapper/1.7.0-28.5/geotools-wrapper-1.7.0-28.5.jar"

#Install necessary python libraries
apt-get -y update

/opt/conda/miniconda3/bin/python -m pip install apache-sedona==1.7.0
