from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Simple Python function
def print_message():
    print("Airflow is running my simple DAG!")

# DAG definition
with DAG(
    dag_id="print_message_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval=None,   # run manually only
    catchup=False,
    tags=["test"],
) as dag:

    task1 = PythonOperator(
        task_id="print_message_task",
        python_callable=print_message,
    )
