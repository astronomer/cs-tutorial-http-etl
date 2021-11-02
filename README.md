# Customer Success REST API ETL Tutorial
This DAG demonstrates how to use the `SimpleHttpOperator`to extract REST API endpoint results in an ETL/ELT process

# Prerequisites:
- Astro CLI
- A free account with [Calendarific](https://calendarific.com/) - we'll be using their API
- Optional: AWS S3 Account (used as a staging area for the REST API endpoint results)
- Optional: Snowflake Instance (used to load staging area items into a Database)

# Steps to Use:
### Run the following in your terminal:
1. `git clone git@github.com:astronomer/cs-tutorial-http-etl.git`
2. `cd cs-tutorial-databricks`
3. `astro d start`

### Add **calendarific_conn** connection to your sandbox
*Please note that if you skip setting up s3 and snowflake, you can view the response from the `rest_api_call` task in your Airflow XCom variables. To view those in the Airflow UI, use the Admin menu and navigate to Admin >> XComs*
1. Go to your sandbox http://localhost:8080/home
2. Navigate to connections (i.e. Admin >> Connections)
3. Add a new connection with the following parameters
    - Connection Id: calendarific_conn
    - Connection Type: HTTP
    - Host: https://calendarific.com/api/v2
    - Password: *your_calendarific_api_key*

Be sure to replace *your_calendarific_api_key* with the api_key associated with your calendarific account. 

**FYI**: After signing up for a free account, you should see this key on your [account dashboard](https://calendarific.com/account)

### Add **my_s3_conn** connection to your sandbox
*Please note that this step is optional for this Demol, if you skip it, you will not be able to run the `upload_to_s3` task*
1. Go to your sandbox http://localhost:8080/home
2. Navigate to connections (i.e. Admin >> Connections)
3. Add a new connection with the following parameters
    - Connection Id: my_s3_conn
    - Connection Type: S3
    - Extra: {"aws_access_key_id": "*your_aws_access_key_id*", "aws_secret_access_key": "*your_aws_secret_access_key*"}

Be sure to replace *your_aws_access_key_id* and *your_aws_secret_access_key* with AWS account credentials that have access to S3

4. In the `http-to-s3-snowflake.py` change the param `bucket_name` in the task `upload_to_s3` to an actual S3 bucket in your AWS account.

### Add **my_snowflake_conn** connection to your sandbox
*Please note that this step is optional for this Demo, if you skip it, you will not be able to run the `copy_full_holidays_to_snowflake` task*
1. Go to your sandbox http://localhost:8080/home
2. Navigate to connections (i.e. Admin >> Connections)
3. Add a new connection with the following parameters
    - Connection Id: my_snowflake_conn
    - Connection Type: Snowflake
    - Host: *your_snowflake_host*
    - Login: *your_snwoflake_login*
    - Password: *your_snowflake_password*
    - Account: *your_snowflake_account*
    - Database: *your_snowflake_database*
    - Region: *your_snowflake_region*
    - Warehouse: *your_snowflake_warehouse*

Replacing the values in italics with the actual connection parameters to your snowflake database

4. In the `http-to-s3-snowflake.py` change the param `schema_name` in the task `copy_full_holidays_to_snowflake` to an actual schema in your Snowflake Database

___
After following these steps, you should be able to run the tasks in the `http-to-s3-to-snowflake`. Enjoy!
