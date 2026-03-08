FROM python:3.10-slim

RUN pip install \
    dagster \
    dagster-graphql \
    dagster-webserver \
    dagster-postgres \
    dagster-docker \
    requests \
    pandas \
    boto3 \
    pyarrow \
    duckdb \
    dbt-core \
    dbt-duckdb

ENV DAGSTER_HOME=/opt/dagster/dagster_home

RUN mkdir -p $DAGSTER_HOME
COPY dagster.yaml workspace.yaml definitions.py $DAGSTER_HOME

WORKDIR /opt/dagster/app
COPY definitions.py .