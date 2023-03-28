#!/usr/bin/env python
# coding: utf-8

from google.cloud import bigquery
from google.cloud import storage
from datetime import datetime
from google.api_core import retry
from google.cloud.exceptions import NotFound
import sys
from config import gcs_bucket_name, crypto_folder, dataset_id, creds


# Set variables
crypto = sys.argv[1]
bucket_name = gcs_bucket_name 
crypto_folder = crypto_folder
dataset_id = dataset_id

# Path to your credentials file
creds_path = creds

# Instantiate a client object
client = bigquery.Client.from_service_account_json(creds_path)

# Set up GCS client object
storage_client = storage.Client.from_service_account_json(creds_path)

# Get current date in YYYYMMDD format
current_date = datetime.now().strftime('%Y-%m-%d')

# Construct GCS URI for the file to be loaded
gcs_uri = f'gs://{bucket_name}/{crypto_folder}/{crypto}/{crypto}_{current_date}.csv'

# Construct table ID for BigQuery table
table_id = f'{crypto}_{current_date}_bq'

# Construct reference to the BigQuery dataset
dataset_ref = client.dataset(dataset_id)

# Define retry object
retry_policy = retry.Retry(
    predicate=retry.if_transient_error,
    deadline=30
)

# Check if table exists, create it if it doesn't
table_ref = dataset_ref.table(table_id)
try:
    table = client.get_table(table_ref)
    print(f'Table {table_id} already exists in {table.dataset_id}. Skipping data load.')
except NotFound:
    schema = [
        bigquery.SchemaField('date', 'DATE', mode='NULLABLE'),
        bigquery.SchemaField('low', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('high', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('open', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('close', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('volume_from', 'FLOAT', mode='NULLABLE'),
        bigquery.SchemaField('volume_to', 'FLOAT', mode='NULLABLE')
    ]
    table = bigquery.Table(table_ref, schema=schema)
    table = client.create_table(table)
    print(f'Created table {table.table_id} in {table.dataset_id}.')
    
    # Construct job configuration
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV,
        field_delimiter=','
    )

    # Construct the BigQuery load job
    load_job = client.load_table_from_uri(
        gcs_uri,
        dataset_ref.table(table_id),
        job_config=job_config
    )

    # Wait for the load job to finish
    load_job.result()

    # Print message upon completion
    print(f'Table {table_id} successfully created and data loaded in BigQuery.')
