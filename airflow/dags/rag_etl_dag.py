import os
import git
import shutil
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def clone_repository(**kwargs):
    github_url = kwargs['dag_run'].conf['github_url']
    repo_name = github_url.split('/')[-1].replace('.git', '')
    clone_dir = f'/tmp/{repo_name}'
    
    if os.path.exists(clone_dir):
        shutil.rmtree(clone_dir)
    
    git.Repo.clone_from(github_url, clone_dir)
    return clone_dir

def parse_files(**kwargs):
    clone_dir = kwargs['ti'].xcom_pull(task_ids='clone_repository')
    file_types = kwargs['dag_run'].conf['file_types']
    output_dir = f'{clone_dir}_parsed'
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    for root, _, files in os.walk(clone_dir):
        for file in files:
            if file.split('.')[-1] in file_types:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, clone_dir)
                dst_path = os.path.join(output_dir, rel_path)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)

    return output_dir

with DAG('rag_etl_dag', default_args=default_args, schedule_interval=None) as dag:
    clone_task = PythonOperator(
        task_id='clone_repository',
        python_callable=clone_repository,
        provide_context=True,
    )

    parse_task = PythonOperator(
        task_id='parse_files',
        python_callable=parse_files,
        provide_context=True,
    )

    clone_task >> parse_task