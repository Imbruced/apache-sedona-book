FROM openrouteservice/openrouteservice:v8.0.0

COPY config /home/ors/config

RUN wget https://download.geofabrik.de/europe/france/ile-de-france-latest.osm.pbf
RUN mv ile-de-france-latest.osm.pbf /home/ors/files/ile-de-france-latest.osm.pbf
RUN apk add --update \
    curl
