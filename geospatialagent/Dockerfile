FROM ghcr.io/astral-sh/uv:python3.12-bookworm

RUN apt-get update && apt-get install wget \
    && mkdir -p /etc/apt/keyrings \
    && wget -O - https://packages.adoptium.net/artifactory/api/gpg/key/public | tee /etc/apt/keyrings/adoptium.asc \
    && echo "deb [signed-by=/etc/apt/keyrings/adoptium.asc] https://packages.adoptium.net/artifactory/deb $(awk -F= '/^VERSION_CODENAME/{print$2}' /etc/os-release) main" | tee /etc/apt/sources.list.d/adoptium.list \
    && apt update \
    && apt install -y temurin-11-jdk

COPY pyproject.toml .
COPY uv.lock .
RUN uv sync

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
EXPOSE 9080
RUN mkdir config
COPY config/spark-defaults.conf config/spark-defaults.conf
ENV SPARK_CONF_DIR=/config

RUN wget https://repo1.maven.org/maven2/org/apache/sedona/sedona-spark-shaded-3.5_2.12/1.8.0/sedona-spark-shaded-3.5_2.12-1.8.0.jar && \
    wget https://repo1.maven.org/maven2/org/datasyslab/geotools-wrapper/1.8.0-33.1/geotools-wrapper-1.8.0-33.1.jar

RUN wget https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.9.2/iceberg-spark-runtime-3.5_2.12-1.9.2.jar
RUN wget https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar

RUN wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar

RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar

ARG JARS_PATH=/.venv/lib/python3.12/site-packages/pyspark/jars
RUN cp sedona-spark-shaded-3.5_2.12-1.8.0.jar ${JARS_PATH} && \
    cp geotools-wrapper-1.8.0-33.1.jar ${JARS_PATH} \
    && cp iceberg-spark-runtime-3.5_2.12-1.9.2.jar ${JARS_PATH} \
    && cp postgresql-42.7.4.jar ${JARS_PATH} \
    && cp aws-java-sdk-bundle-1.12.262.jar ${JARS_PATH} \
    && cp hadoop-aws-3.3.4.jar ${JARS_PATH}

COPY src ./src
COPY app.py .

ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]
