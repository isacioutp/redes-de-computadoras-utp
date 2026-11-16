FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      tcpdump iproute2 traceroute iputils-ping curl \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir flask psycopg2-binary
COPY app.py /app/app.py
WORKDIR /app
EXPOSE 5000
CMD ["python", "app.py"]