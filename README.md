# Cryptocurrency Data Engineering Project
# Problem
The aim of this project was to ingest historical **daily** cryptocurrency data for multiple cryptocurrencies. This is to be ingested into google cloud storage, uploaded into Google BigQuery, transformed using Data Build Tool and loaded back into BigQuery, and then visualised within Google Sheets using the BigQuery Data Connector.
 # Repo Guide
This repository contains all the files and code necessary to run a data engineering project that pulls cryptocurrency data from an API, stores it in a data warehouse, processes it with DBT, and makes it available for analysis in a business intelligence tool.

The project is designed to be modular and scalable, allowing for easy adaptation to different data sources and use cases. It includes scripts for pulling data from the CyptoCompare API and storing it in a PostgreSQL database, as well as a set of DBT models for transforming the raw data into a clean, structured format. Additionally, the repository includes documentation and sample queries for accessing and analyzing the data in a business intelligence tool.

The project is built using open-source tools and frameworks, including Python, PostgreSQL and DBT Cloud. It is intended for educational purposes and can be used as a starting point for learning about data engineering and cryptocurrency data analysis.

Repository Contents:

Project directory that contains the scripts required to run the full ETL Process.

DBT directory containing DBT models and related files for processing the data

README.md file providing an overview of the project and instructions for getting started

# Instructions
To use this pipeline, one must have access to:
- DBT Cloud API
- Google Cloud Platform (Google Cloud Storage and Google BigQuery)
- Prefect Cloud

In order to use this ETL pipeline, one must follow the following steps:
1. Go to https://www.cryptocompare.com/ and create an account. Click the 'API' tab at the top of the website, and generate your own personal API. This should be free. Save the API in config.py as ```cryptocompare_api_key```
2. Go to Google Cloud Platform and ensure you have a new project created. Then go to _IAM and admin_ and click service accounts. Ensure it has access as a BigQuery Admin, as well as Storage Admin. Create a key for this service account and download is as a json. This should be stored within the project folder. (Ensure this is not uploaded to your repo). This can be done by adding my-project-key.json in your gitignore file.
3. In DBT Cloud, configure your project to access the DBT folder within this github repo. This can be done by using git clone on this repository, making sure to make 'DBT' as the project subdirectory. (Please note, you will need to have a **paid** developer subscription to DBT cloud for this method to work).
4. Within DBT, create a Job that runs this project. In my project, I simply used the job dbt run. This is also where you will get your prefect_cloud_job_id for the config.py file:


![image](https://user-images.githubusercontent.com/122522521/228802505-766fd788-3e63-410a-b8c6-6d843236c1be.png)


Note that it is the final 6 digits of the URL.

5. In Prefect Cloud, ensure you create a DBT credentials block so that you can successfully ping the DBT Cloud API. This can be done using the code:
```python

from prefect_dbt.cloud import DbtCloudCredentials

DbtCloudCredentials(
    api_key="API-KEY-PLACEHOLDER",
    account_id="ACCOUNT-ID-PLACEHOLDER"
).save("BLOCK-NAME-PLACEHOLDER")

```

This should then be used in config.py as ```prefect_cloud_dbt_block_name```

6. Run ```python prefect_crypto_flow.py``` for the full ETL process.

This is the final cryptocurrency dashboard:

![image](https://user-images.githubusercontent.com/122522521/228805080-97bf03ea-455b-4fbc-9d40-8a037db492f2.png)

![image](https://user-images.githubusercontent.com/122522521/228805282-5c85e734-cabc-4f27-b460-c155d24c5047.png)


Here is the link to my resultant cryptocurrency data dashboard:
https://docs.google.com/spreadsheets/d/1cO7mWZXv4BG1BCGUdTxBcyGvb9097Z04P4yzcj9QrDE/edit?usp=sharing

This was used as a proof of concept for a business idea. Unfortunately I cannot allow anyone to refresh this as it will cost money, so the drop down (which uses a parameter custom query) will not work (but rest assured, it does).

Contributors:

Lachlan Casey
