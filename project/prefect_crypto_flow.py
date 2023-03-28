#!/usr/bin/env python
# coding: utf-8

# In[8]:


import prefect
from prefect import task, flow
from pathlib import Path
from prefect.task_runners import SequentialTaskRunner
import os
from prefect_dbt.cli.commands import DbtCoreOperation
from prefect_dbt.cloud import DbtCloudCredentials, DbtCloudJob
from prefect_dbt.cloud.jobs import run_dbt_cloud_job
from prefect_dbt.cloud.jobs import trigger_dbt_cloud_job_run
from config import prefect_cloud_api_key, prefect_cloud_dbt_block_name, prefect_cloud_job_id, prefect_crypto_list_for_etl


# set the API key as an environment variable
os.environ["PREFECT__CLOUD__API_KEY"] = prefect_cloud_api_key

# In[2]:
dbt_cloud_credentials = DbtCloudCredentials.load(prefect_cloud_dbt_block_name)

@task
def ingest_crypto_data(crypto: str):
    command = f"python Crypto_data_ingest.py {crypto}"
    os.system(command)


# In[3]:


@task
def load_crypto_data_to_bq(crypto: str):
    command = f"python Crypto_data_gcs_to_bq.py {crypto}"
    os.system(command)


# In[14]:


@flow(task_runner=SequentialTaskRunner())
def crypto_flow(crypto: str):
    ingest_crypto_data(crypto=crypto)

    # Load data from GCS to BigQuery for each crypto
    load_crypto_data_to_bq(crypto=crypto)

    #note that if no parameters are given, it defaults to BTC and ETH


# In[9]:


@flow
def run_dbt_job_flow():
        trigger_dbt_cloud_job_run(
        dbt_cloud_credentials=dbt_cloud_credentials,
        job_id=prefect_cloud_job_id
    )


# In[10]:


@flow()
def etl_parent_flow(cryptos: list[str] = ["BTC","ETH"]):
    for crypto in cryptos:
        crypto_flow(crypto=crypto)
    run_dbt_job_flow()


# In[11]:


if __name__ == "__main__":
    cryptos = prefect_crypto_list_for_etl
    etl_parent_flow(cryptos)

