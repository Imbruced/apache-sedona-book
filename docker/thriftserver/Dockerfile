ARG SPARK_VERSION=3.5.4
ARG SPARK_VERSION_MAJOR=3.5
ARG SCALA_VERSION=2.12

FROM spark:${SPARK_VERSION}-scala${SCALA_VERSION}-java11-python3-ubuntu
USER root

ARG SPARK_VERSION=3.5.4
ARG SPARK_VERSION_MAJOR=3.5
ARG SCALA_VERSION=2.12
ARG SEDONA_VERSION=1.7.0

WORKDIR /opt/spark
RUN wget https://repo1.maven.org/maven2/org/apache/sedona/sedona-spark-shaded-${SPARK_VERSION_MAJOR}_${SCALA_VERSION}/${SEDONA_VERSION}/sedona-spark-shaded-${SPARK_VERSION_MAJOR}_${SCALA_VERSION}-${SEDONA_VERSION}.jar
RUN wget https://repo1.maven.org/maven2/org/datasyslab/geotools-wrapper/${SEDONA_VERSION}-28.5/geotools-wrapper-${SEDONA_VERSION}-28.5.jar
RUN cp sedona-spark-shaded-${SPARK_VERSION_MAJOR}_${SCALA_VERSION}-${SEDONA_VERSION}.jar /opt/spark/jars
RUN cp geotools-wrapper-${SEDONA_VERSION}-28.5.jar /opt/spark/jars
RUN pip3 install apache-sedona
ENV SPARK_HOME=/opt/spark

RUN mkdir -p /opt/spark/spark-warehouse/raw
COPY data/observations ./spark-warehouse/raw/observations
COPY data/borders ./spark-warehouse/raw/borders
COPY scripts ./


EXPOSE 10001
EXPOSE 4040-4050
CMD ["/bin/sh", "./start.sh"]
