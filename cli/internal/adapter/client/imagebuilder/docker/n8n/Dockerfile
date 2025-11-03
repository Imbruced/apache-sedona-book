FROM docker.n8n.io/n8nio/n8n
USER root
RUN apk add curl

USER node
COPY entrypoint.sh entrypoint.sh
ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]