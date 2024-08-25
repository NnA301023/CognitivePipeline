FROM apache/airflow:2.5.1

USER root

RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean

USER airflow

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt