drop table if exists {{ params.schema_name }}.{{ params.table_name }};
create table {{ params.schema_name }}.{{ params.table_name }} (calendarific_holidays_2019 variant);
copy into {{ params.schema_name }}.{{ params.table_name }} from 's3://airflow-success/demo-files/http-to-s3-to-snowflake-demo/holidays.json'
file_format = (type = json)
;