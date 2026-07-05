from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

# This is your pipeline definition
with DAG(
    dag_id="polymarket_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@hourly",     # runs automatically every hour,     --- day 5     # None = manual trigger only (for now)
    catchup=False,
    tags=["polymarket"],
) as dag:

    # Task 1: run your fetch+clean+load script
    fetch_and_load = BashOperator(
        task_id="fetch_and_load",
        bash_command="cd /Users/u1618628/Documents/polymarket-pipeline/src && python3 fetch.py",
    )