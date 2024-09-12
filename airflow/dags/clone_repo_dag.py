import git
from airflow import DAG
from datetime import datetime
from airflow.operators.python_operator import PythonOperator


def clone_repo(**kwargs):
    repo_url = kwargs['dag_run'].conf.get('repo_url')
    branch = kwargs['dag_run'].conf.get('branch')
    destination = kwargs['dag_run'].conf.get('destination')
    
    if not repo_url or not destination:
        raise ValueError("Repository URL and destination are required")
    
    git.Repo.clone_from(repo_url, destination, branch=branch)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

dag = DAG(
    'clone_repo',
    default_args=default_args,
    description='Clone a git repository',
    schedule_interval=None,
)

clone_task = PythonOperator(
    task_id='clone_repository',
    python_callable=clone_repo,
    provide_context=True,
    dag=dag,
)

clone_task