FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      tcpdump iproute2 traceroute iputils-ping curl \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir flask
COPY server.py /app/server.py
WORKDIR /app
EXPOSE 5000
CMD ["python", "server.py"]