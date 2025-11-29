FROM ghcr.io/osgeo/gdal:ubuntu-full-3.12.0

RUN apt-get update
RUN apt-get install -y python3-pip

RUN pip3 install --break-system-packages uv

RUN mkdir -p /home/ubuntu/sedona-ai

WORKDIR /home/ubuntu/sedona-ai

COPY pyproject.toml ./

RUN uv sync

RUN apt-get install -y openjdk-11-jdk
RUN update-java-alternatives --set java-1.11.0-openjdk-arm64
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV JARS_DIR=/home/ubuntu/sedona-ai/.venv/lib/python3.12/site-packages/pyspark/jars
ENV SEDONA_VERSION=1.8.0
ENV GEOTOOLS_VERSION=1.8.0-33.1
ENV SPARK_VERSION_MAJOR=3.5
ENV SCALA_VERSION=2.12

RUN apt-get install -y wget

RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar
RUN wget https://repo1.maven.org/maven2/org/apache/sedona/sedona-spark-shaded-${SPARK_VERSION_MAJOR}_${SCALA_VERSION}/${SEDONA_VERSION}/sedona-spark-shaded-${SPARK_VERSION_MAJOR}_${SCALA_VERSION}-${SEDONA_VERSION}.jar && \
    wget https://repo1.maven.org/maven2/org/datasyslab/geotools-wrapper/${GEOTOOLS_VERSION}/geotools-wrapper-${GEOTOOLS_VERSION}.jar && \
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar


RUN cp aws-java-sdk-bundle-1.12.262.jar ${JARS_DIR} && \
    cp hadoop-aws-3.3.4.jar ${JARS_DIR} && \
    cp sedona-spark-shaded-${SPARK_VERSION_MAJOR}_${SCALA_VERSION}-${SEDONA_VERSION}.jar ${JARS_DIR} && \
    cp geotools-wrapper-${GEOTOOLS_VERSION}.jar ${JARS_DIR}

ENTRYPOINT ["uv", "run", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--NotebookApp.token=''"]
