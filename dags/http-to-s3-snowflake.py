import json
import io
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime

def upload_json_to_s3(xcom_task_id, bucket_name, key="out", replace=True, **context):
    json_dict = context['ti'].xcom_pull(task_ids=f'{xcom_task_id}')
    s3_hook = S3Hook(aws_conn_id="my_s3_conn")

    with io.BytesIO() as in_mem_file:
        in_mem_file.write(json.dumps(json_dict).encode())
        in_mem_file.seek(0)
        s3_hook._upload_file_obj(
            file_obj=in_mem_file,
            key=key,
            bucket_name=bucket_name,
            replace=replace
        )

with DAG('http-to-s3-to-snowflake',
         start_date=datetime(2021, 10, 25),
         max_active_runs=3,
         schedule_interval=None,
         template_searchpath="/usr/local/airflow/include/http-to-s3-to-snowflake/"
         ) as dag:

    start = DummyOperator(
        task_id='start'
    )

    t1 = SimpleHttpOperator(
        # https://calendarific.com/api-documentation
        # Host: https://calendarific.com/api/v2
        task_id="rest_api_call",
        http_conn_id="calendarific_conn",
        endpoint="/holidays",
        method="GET",
        data={
            "api_key": "{{ conn.calendarific_conn.password }}",
            "country": "US",
            "year": "2019"
        },
        response_filter=lambda response: response.json()['response']['holidays']
    )

    t2 = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_json_to_s3,
        op_kwargs={
            "xcom_task_id": "rest_api_call",
            "bucket_name": "enter-your-bucket-here",
            "key": "demo-files/http-to-s3-to-snowflake-demo/holidays.json",
            "replace": True
        }
    )

    t3 = SnowflakeOperator(
        task_id=f"copy_full_holidays_to_snowflake",
        snowflake_conn_id="my_snowflake_conn",
        sql=f"sql/calendarific_holidays_2019.sql",
        params={
            "schema_name": "enter-your-schema-here",
            "table_name": "calendarific_holidays_2019"
        }
    )

    finish = DummyOperator(
        task_id='finish'
    )

    start >> t1 >> t2 >> t3 >> finish