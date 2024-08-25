import requests
import streamlit as st

AIRFLOW_URL = "http://airflow-webserver:8080/api/v1"
AIRFLOW_USERNAME = "admin"
AIRFLOW_PASSWORD = "admin"

def trigger_dag(dag_id, github_url, file_types):
    endpoint = f"{AIRFLOW_URL}/dags/{dag_id}/dagRuns"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "conf": {
            "github_url": github_url,
            "file_types": file_types
        }
    }
    response = requests.post(endpoint, json=data, headers=headers, auth=(AIRFLOW_USERNAME, AIRFLOW_PASSWORD))
    return response.status_code == 200

st.title("GitHub ETL Pipeline")
github_url = st.text_input("Enter GitHub Repository URL")
file_types = st.multiselect("Select file types to parse", ["json", "md", "yaml", "pdf"])

if st.button("Trigger ETL Pipeline"):
    if github_url and file_types:
        if trigger_dag("github_etl_dag", github_url, file_types):
            st.success("ETL pipeline triggered successfully!")
        else:
            st.error("Failed to trigger ETL pipeline. Please check Airflow logs.")
    else:
        st.warning("Please enter a GitHub URL and select at least one file type.")