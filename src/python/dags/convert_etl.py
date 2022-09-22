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

import os

import numpy as np
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

DATA_PATH = "s3://mlflow/data/"
OUTPUT_PATH = 's3://mlflow/feature_engineering/'
S3_ENDPOINT_URL = 'http://s3-faker:4566'

default_args = {
    'owner': 'steve.tran',
    'depends_on_past': False,
    'email': ['steve.tran@gmail.com'],
    'email_on_failure': False,
    'retries': 0
}

class OrdinalEncoder:
    """
    Ordinal Encoder. Transform ID features into integer-based array
    Support nan/empty values, convert from start_from index
    """

    def __init__(self, start_from=1, unknown=0):
        self.vocabs = {}
        self.inv = []

        self.start_from = start_from
        self.unknown = unknown

        self._fitted = False

    def __len__(
        self,
    ):
        return len(self.inv)

    def fit(self, X):

        import numpy as np

        X_uniq = np.unique(X)

        self.inv = [0] * (len(X_uniq) + self.start_from)

        for idx, item in enumerate(X_uniq):
            self.vocabs[item] = self.start_from + idx
            self.inv[self.start_from + idx] = item

        self.inv = np.array(self.inv)

        self._fitted = True

        return self

    def transform(self, X):
        import numpy as np

        if len(X) == 0:
            return []

        if isinstance(X[0], (list, np.ndarray)):
            res = []
            for idx in range(len(X)):
                tmp = [self.vocabs.get(item) for item in X[idx] if item in self.vocabs]

                res.append(tmp)
            return res
        else:
            return np.array(
                [self.vocabs.get(item, self.unknown) for item in X], dtype="int"
            )

    def fit_transform(self, X):
        return self.fit(X).transform(X)

    def inverse_transform(self, X):
        if len(X) == 0:
            return []

        X = np.array(X, dtype="int")

        return self.inv[X]

    @property
    def n_classes_(self):
        return len(self.inv)

    def export(self):
        return self.vocabs

    def load_vocab(self, vocabs: dict):
        self.vocabs = vocabs

        for k, v in self.vocabs.items():
            self.inv[v] = k

        return self

def convert_store_metadata():
    import pandas as pd
    
    df_store = pd.read_csv(DATA_PATH + "data_metadata_store.csv",storage_options={
        "client_kwargs":{
            'endpoint_url': S3_ENDPOINT_URL
        }
    })
    store_type_encoder = OrdinalEncoder(start_from=0)
    df_store["STORE_TYPE"] = store_type_encoder.fit_transform(df_store["STORE_TYPE"].fillna("unk"))
    df_store["REGION_ID"] = df_store["REGION_ID"].fillna(-1)
    df_store["STORE_SIZE"] = df_store["STORE_SIZE"].fillna(0)
    df_store["created_at"] = pd.to_datetime("2022-01-01",utc=True)
    df_store.to_parquet(OUTPUT_PATH + "store_metadata.pq", index=False, storage_options={
        "client_kwargs":{
            'endpoint_url': S3_ENDPOINT_URL
        }
    })

def convert_product_metadata():
    import pandas as pd
    df_product = pd.read_csv(DATA_PATH + "data_metadata_product.csv",storage_options={
        "client_kwargs":{
            'endpoint_url': S3_ENDPOINT_URL
        }
    })

    product_metadata_encoder = OrdinalEncoder()
    df_product["PRODUCT_METADATA"] = product_metadata_encoder.fit_transform(df_product["PRODUCT_METADATA"].fillna("unk"))
    df_product["created_at"] = pd.to_datetime("2022-01-01",utc=True)
    df_product.to_parquet(OUTPUT_PATH + "product_metadata.pq", index=False, storage_options={
            "client_kwargs":{
                'endpoint_url': S3_ENDPOINT_URL
            }
    })

def compute_store_and_product_stats():
    import pandas as pd
    df_order = pd.read_csv(DATA_PATH + "data_order.csv", parse_dates=["CHECKOUT_DATE"], storage_options={
        "client_kwargs":{
            'endpoint_url': S3_ENDPOINT_URL
        }
    }).sort_values(by=["CHECKOUT_DATE"])
    df_product = pd.read_csv(DATA_PATH + "data_metadata_product.csv",storage_options={
        "client_kwargs":{
            'endpoint_url': S3_ENDPOINT_URL
        }
    }) 
    df_store = pd.read_csv(DATA_PATH + "data_metadata_store.csv",storage_options={
        "client_kwargs":{
            'endpoint_url': S3_ENDPOINT_URL
        }
    })    

    df_order_joint = df_order[["ORDER_ID", "STORE_ID", "QUANTITY", "PRODUCT_ID", "CHECKOUT_DATE"]]\
        .merge(df_product, on=["PRODUCT_ID"], how="left")\
        .merge(df_store, on=["STORE_ID"], how="left").copy(deep=True)
    
    df_store_stat = df_order_joint.groupby(["STORE_ID", "CHECKOUT_DATE"]).agg(
        {
            "PRODUCT_METADATA":"nunique",
            "PRODUCT_ID": "nunique",
            "QUANTITY": "sum",
        }
    ).reset_index()
    for lag in [1, 2]:
        df_store_stat["num_product_types_prev_{}".format(lag)] = df_store_stat.groupby(["STORE_ID"])["PRODUCT_METADATA"].shift(lag)
        df_store_stat["num_products_prev_{}".format(lag)] = df_store_stat.groupby(["STORE_ID"])["PRODUCT_ID"].shift(lag)
        df_store_stat["total_quantities_prev_{}".format(lag)] = df_store_stat.groupby(["STORE_ID"])["QUANTITY"].shift(lag)    
    
    df_store_stat["CHECKOUT_DATE"] = pd.to_datetime(df_store_stat["CHECKOUT_DATE"], utc=True)
    df_store_stat.to_parquet(OUTPUT_PATH + "store_stats.pq", index=False, storage_options={
        "client_kwargs":{
            'endpoint_url': S3_ENDPOINT_URL
        }
    })

    df_order_store = df_order_joint.groupby(["STORE_ID", "PRODUCT_ID", "CHECKOUT_DATE"])["QUANTITY"].sum().reset_index()
    for i in [1, 2, 3, 4, 5, 6, 7]:
        df_order_store["quantity_prev_{}".format(i)] = df_order_store.groupby(["STORE_ID", "PRODUCT_ID"])["QUANTITY"].shift(i)
    
    df_order_store.to_parquet(OUTPUT_PATH + "store_product_stat.pq", index=False, storage_options={
        "client_kwargs":{
            'endpoint_url': S3_ENDPOINT_URL
        }
    })

with DAG(
    dag_id="feature_engineering_etl",
    default_args=default_args,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
) as dag:
    convert_store_metadata_op = PythonOperator(
        task_id="convert_store_metadata",
        python_callable=convert_store_metadata
    )

    convert_product_metadata_op = PythonOperator(
        task_id="convert_product_metadata_op",
        python_callable=convert_product_metadata,
    )

    compute_store_and_product_stats_op = PythonOperator(
        task_id="compute_store_and_product_stats_op",
        python_callable=compute_store_and_product_stats,
    )
