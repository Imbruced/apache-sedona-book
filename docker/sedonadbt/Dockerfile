FROM apache/sedona:1.7.1

RUN pip install dbt-core dbt-spark "dbt-spark[PyHive]"

COPY profiles.yaml /root/.dbt/profiles.yml