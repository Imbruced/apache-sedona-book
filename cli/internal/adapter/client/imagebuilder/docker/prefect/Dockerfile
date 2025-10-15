FROM prefecthq/prefect:3.4.23-python3.12

ENV SEDONA_VERSION=1.7.2
ENV GEOTOOLS_VERSION=28.5
ENV SPARK_VERSION=3.5
ENV SCALA_VERSION=2.12

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install wget \
    && mkdir -p /etc/apt/keyrings \
    && wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /etc/apt/keyrings/adoptium.asc \
    && echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list \
    && apt update \
    && apt install -y temurin-11-jdk

RUN wget https://repo1.maven.org/maven2/org/apache/sedona/sedona-spark-shaded-${SPARK_VERSION}_${SCALA_VERSION}/${SEDONA_VERSION}/sedona-spark-shaded-${SPARK_VERSION}_${SCALA_VERSION}-${SEDONA_VERSION}.jar && \
    wget https://repo1.maven.org/maven2/org/datasyslab/geotools-wrapper/${SEDONA_VERSION}-${GEOTOOLS_VERSION}/geotools-wrapper-${SEDONA_VERSION}-${GEOTOOLS_VERSION}.jar


RUN cp sedona-spark-shaded-3.5_2.12-1.7.2.jar /usr/local/lib/python3.12/site-packages/pyspark/jars && \
    cp geotools-wrapper-1.7.2-28.5.jar /usr/local/lib/python3.12/site-packages/pyspark/jars