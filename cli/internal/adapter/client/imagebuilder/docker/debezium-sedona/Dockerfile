FROM quay.io/debezium/connect:3.2.1

COPY create-connector.sh ./create-connector.sh

COPY entrypoint.sh ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
