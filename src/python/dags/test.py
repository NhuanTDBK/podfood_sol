#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Example DAG demonstrating the usage of DateTimeBranchOperator with datetime as well as time objects as
targets.
"""
from __future__ import annotations

import pendulum
from airflow import DAG
from airflow.operators.datetime import BranchDateTimeOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'nhuan.tran',
    'depends_on_past': False,
    'email': ['nhuan.tran@onemount.com'],
    'email_on_failure': False,
    'retries': 0
}

dag1 = DAG(
    dag_id="example_branch_datetime_operator_test",
    default_args=default_args,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)

def check_pandas():
    import pandas as pd
    path = "s3://mlflow/data/data_order.csv"
    df = pd.read_csv(path, parse_dates=["CHECKOUT_DATE"], storage_options={
        "client_kwargs":{
            'endpoint_url': 'http://s3-faker:4566'
        }
    }).sort_values(by=["CHECKOUT_DATE"])

    print(df.head())

# [START howto_branch_datetime_operator]
empty_task_11 = EmptyOperator(task_id='date_in_range', dag=dag1)
empty_task_21 = EmptyOperator(task_id='date_outside_range', dag=dag1)

task1 = PythonOperator(
    task_id="test_dag_pandas",
    python_callable=check_pandas,
)

cond1 = BranchDateTimeOperator(
    task_id='datetime_branch',
    follow_task_ids_if_true=['date_in_range'],
    follow_task_ids_if_false=['date_outside_range'],
    target_upper=pendulum.datetime(2020, 10, 10, 15, 0, 0),
    target_lower=pendulum.datetime(2020, 10, 10, 14, 0, 0),
    dag=dag1,
)

# Run empty_task_1 if cond1 executes between 2020-10-10 14:00:00 and 2020-10-10 15:00:00
task1 >> cond1 >> [empty_task_11, empty_task_21]
# [END howto_branch_datetime_operator]
