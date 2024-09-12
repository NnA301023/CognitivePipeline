FROM apache/airflow:2.6.3-python3.9
USER root
RUN apt-get update && apt-get install -y git
USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt