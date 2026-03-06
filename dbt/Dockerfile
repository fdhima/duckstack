FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl unzip && \
    pip install dbt-core dbt-duckdb duckdb && \
    curl -fsSL https://github.com/duckdb/duckdb/releases/latest/download/duckdb_cli-linux-amd64.zip -o /tmp/duckdb.zip && \
    unzip /tmp/duckdb.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/duckdb && \
    rm /tmp/duckdb.zip && \
    apt-get remove -y curl unzip && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app/dbt
