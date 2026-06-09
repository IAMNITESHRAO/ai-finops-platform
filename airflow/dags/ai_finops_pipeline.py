from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="ai_finops_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["ai-finops"],
) as dag:

    start = BashOperator(
        task_id="start",
        bash_command="echo 'AI FinOps Pipeline Started'"
    )

    bronze = BashOperator(
        task_id="check_project",
        bash_command="ls -la /opt/project"
    )

    end = BashOperator(
        task_id="end",
        bash_command="echo 'Pipeline Finished'"
    )

    start >> bronze >> end