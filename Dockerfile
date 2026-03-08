# FROM python:3.10-slim

# RUN pip install \
#     dagster \
#     dagster-graphql \
#     dagster-webserver \
#     dagster-postgres \
#     dagster-docker \
#     requests \
#     pandas \
#     boto3 \
#     pyarrow \
#     duckdb \ 
#     dbt-core \
#     dbt-duckdb

# ENV DAGSTER_HOME=/opt/dagster/dagster_home
# RUN mkdir -p $DAGSTER_HOME
# COPY dagster.yaml workspace.yaml $DAGSTER_HOME

# WORKDIR /opt/dagster/app
# COPY definitions.py .

# EXPOSE 3000
# HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
#   CMD curl -f http://0.0.0.0:3000/server_info || exit 1

# CMD ["dagster", "dev", "-h", "0.0.0.0", "-p", "3000", "-f", "definitions.py"]
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