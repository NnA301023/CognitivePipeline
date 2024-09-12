import json
import requests
import streamlit as st


AIRFLOW_API_URL = "http://airflow-webserver:8080/api/v1"

st.title("Repository Cloner")

repo_url = st.text_input("Enter repository URL:")
branch = st.text_input("Enter branch name (optional):")
destination = st.text_input("Enter destination folder:")

if st.button("Clone Repository"):
    dag_run_data = {
        "conf": {
            "repo_url": repo_url,
            "branch": branch,
            "destination": destination
        }
    }
    
    response = requests.post(
        f"{AIRFLOW_API_URL}/dags/clone_repo/dagRuns",
        json=dag_run_data,
        headers={"Content-Type": "application/json"},
        auth=("admin", "airflow")
    )
    
    if response.status_code == 200:
        st.success("Repository cloning job triggered successfully!")
    else:
        st.error(f"Failed to trigger job. Status code: {response.status_code}")