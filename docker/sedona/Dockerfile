FROM apache/sedona:1.7.2

RUN wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar && \
    wget https://repo1.maven.org/maven2/org/apache/sedona/sedona-spark-shaded-3.5_2.12/1.7.2/sedona-spark-shaded-3.5_2.12-1.7.2.jar && \
    wget https://repo1.maven.org/maven2/org/datasyslab/geotools-wrapper/1.7.2-28.5/geotools-wrapper-1.7.2-28.5.jar


RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar

RUN cp aws-java-sdk-bundle-1.12.262.jar /opt/spark/jars && \
    cp hadoop-aws-3.3.4.jar /opt/spark/jars

# add conifguration files
COPY s3-conf.conf ./
COPY apply.sh ./

CMD ["/bin/bash", "./apply.sh"]
