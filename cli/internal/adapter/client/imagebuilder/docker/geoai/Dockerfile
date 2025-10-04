FROM ghcr.io/osgeo/gdal:ubuntu-full-3.11.0

RUN apt-get update && apt-get install -y python3-pip

RUN pip3 install --break-system-packages uv

RUN mkdir -p /home/ubuntu/sedona-ai

WORKDIR /home/ubuntu/sedona-ai

COPY pyproject.toml uv.lock ./

RUN uv sync

RUN apt-get install -y openjdk-11-jdk
RUN update-java-alternatives --set java-1.11.0-openjdk-arm64
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64

ENTRYPOINT ["uv", "run", "jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--allow-root", "--NotebookApp.token=''"]
