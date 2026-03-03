# Project Idea: Local-First Open-Source Data Platform (Zero-Cost)

## Overview
Build a production-grade analytics platform that runs entirely on your local machine using Docker. This demonstrates you can architect a "Modern Data Stack" (MDS) using only Open Source Software (OSS), avoiding all cloud costs while showing mastery of complex integration.

## The "Zero-Cost" Tech Stack
*   **Infrastructure:** Docker & Docker Compose (orchestrating the entire stack).
*   **Ingestion:** Python (Custom Scrapers or Open-Meteo/OpenAQ APIs).
*   **Storage (The Lake):** MinIO (S3-compatible local object storage).
*   **Warehouse (The Brain):** DuckDB (High-performance OLAP, currently the #1 "hot" skill).
*   **Transformation:** dbt-core (Open-source SQL modeling).
*   **Orchestration:** Dagster (Modern orchestrator with Asset-based lineage).
*   **Visualization:** Evidence.dev (Markdown-based BI) or Apache Superset.
*   **Quality:** Soda Core or dbt-tests.

## Core Requirements
1.  **Containerized Environment:** Everything MUST run via a single `docker-compose.yml` file. This proves you understand networking and container orchestration.
2.  **API to MinIO (Bronze):** Build a Python script that pulls real-time data (e.g., Global Air Quality from OpenAQ or Open-Meteo) and saves it as Parquet files into a MinIO bucket.
3.  **The DuckDB Lakehouse:** 
    *   Use **DuckDB** to read directly from MinIO Parquet files.
    *   Implement a **Medallion Architecture** (Raw -> Clean -> Aggregate) using **dbt-core**.
4.  **Asset-Based Orchestration:** Use **Dagster** to manage the pipeline. Define "Software Defined Assets" so recruiters can see the visual lineage from API to Dashboard.
5.  **Data Quality as Code:** Implement schema validation and "freshness" checks using dbt-tests to ensure the local warehouse doesn't ingest corrupt data.
6.  **Performance Tuning:** Demonstrate DuckDB's speed by processing at least 1 million rows of historical data (available via public datasets like NYC Taxi or NOAA Weather).