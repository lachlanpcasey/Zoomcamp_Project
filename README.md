# Cryptocurrency Data Engineering Project [Zoomcamp]
## Table of contents
- [Project Purpose](#project-purpose)
- [ETL Pipeline](#etl-pipeline)
- [Repo Guide](#repo-guide)
- [Requirements](#requirements)
- [How to run](#how-to-run)
- [Dashboard](#dashboard)

## Purpose <a name="project-purpose"></a>
The aim of this project was to ingest historical **daily** cryptocurrency data for multiple cryptocurrencies. This is to be ingested into google cloud storage, uploaded into Google BigQuery, transformed using Data Build Tool and loaded back into BigQuery, and then visualised within Google Sheets using the BigQuery Data Connector.
I want to be able to analyse the market share of the cryptocurrencies Bitcoin, Ethereum, Litecoin, XRP and Ethereum Name Service by volume traded in USD, as well as analyse the price movements of individual cryptocurrencies.

## ETL Pipeline

![Crypto Data Engineering Project](https://user-images.githubusercontent.com/122522521/229351796-0664d37e-6915-4db7-b431-2f3b1391d755.png)


## Repo Guide
This repository contains all the files and code necessary to run a data engineering project that pulls cryptocurrency data from an API, stores it in a data warehouse, processes it with DBT, and makes it available for analysis in a business intelligence tool.

The project is designed to be modular and scalable, allowing for easy adaptation to different data sources and use cases. It includes scripts for pulling data from the CyptoCompare API and storing it in a PostgreSQL database, as well as a set of DBT models for transforming the raw data into a clean, structured format. Additionally, the repository includes documentation and sample queries for accessing and analyzing the data in a business intelligence tool.

The project is built using open-source tools and frameworks, including Python, PostgreSQL and DBT Cloud. It is intended for educational purposes and can be used as a starting point for learning about data engineering and cryptocurrency data analysis.

Repository Contents:

Project directory that contains the scripts required to run the full ETL Process.

DBT directory containing DBT models and related files for processing the data.

README.md file providing an overview of the project and instructions for getting started.

## Requirements
To use this pipeline, one must have access to:
- DBT Cloud API (Paid)
- Google Cloud Platform (Google Cloud Storage and Google BigQuery) (Paid)
- Prefect Cloud (Free)
- Docker (Free)
- Cryptocompare API (Free)

## Configuration
In order to make sure you can run this pipeline, you must complete config.py in the project folder.
Here is a list of variables, with an explanation of each one:

```cryptocompare_api_key```: The API key for your account at https://www.cryptocompare.com/

```gcs_bucket_name```: Your bucket name in Google Cloud Storage.

```prefect_cloud_api_key```: Your API key in Prefect Cloud 2.

```prefect_cloud_dbt_block_name```: The block name of your prefect cloud dbt block. This can be whatever you like, and will rename any existing dbt cloud credentials you have saved in Prefect Cloud 2.

```dbt_api_key```: Your DBT Cloud API Key. This requires a paid monthly subscription to DBT Cloud.

```dbt_account_id```: Your DBT Cloud Account ID.

```dbt_job_id```: The job ID you want to run in DBT cloud. 

```prefect_crypto_list_for_etl```: A list of cryptocurrencies you want to use for your pipeline. I used ["BTC","ETH","LTC","XRP","ENS"].

```crypto_folder```: The name of your folder within your Google Cloud Storage Bucket.

```dataset_id```: The name of your dataset within Google BigQuery.

```creds```: The name of your json file with your Google Cloud Project service account credentials. Please keep this as creds.json.

In order to get these variables, follow the instructions in [How to run](#how-to-run).

## How to run
In order to use this ETL pipeline, one must follow the following steps:
1. Go to https://www.cryptocompare.com/ and create an account. Click the 'API' tab at the top of the website, and generate your own personal API. This should be free. Save the API in config.py as ```cryptocompare_api_key```
2. Go to Google Cloud Platform and ensure you have a new project created. Then go to _IAM and admin_ and click service accounts. Create a service account, and ensure it has access as a BigQuery Admin, as well as Storage Admin. Create a key for this service account and download it as a json. Copy and paste this file into the creds.json file located in the project directory. Be sure to include this file in gitignore if you are managing your code through github, otherwise others will have access to this confidential information.
3. Then, within Google Cloud Platform go to cloud storage -> buckets and create a new bucket. This is where your crypto csv data will be stored. It will be used as your Data Lake. The name of this bucket should be put in your config.py as ```gcs_bucket_name```.
4. Then, create a folder within this bucket. I called mine crypto_data. This should be added in your config.py as ```crypto_folder ```.
5. Next, go to the BigQuery tab within Google Cloud Project and click SQL Workspace. You should see your project name. Next to the this, click the 3 dots and press _Create dataset_. This will be what is added to your config.py as ```dataset_id```. This is where your raw data will be populated in your data warehouse.
6. In DBT Cloud, configure your project to access the DBT folder within this github repo. This can be done by using git clone on this repository, making sure to make 'DBT' as the project subdirectory. (Please note, you will need to have a **paid** developer subscription to DBT cloud for this method to work).
7. Within DBT, create a Job that runs this project. In my project, I simply used the job dbt run. This is also where you will get your dbt_job_id for the config.py file:


![image](https://user-images.githubusercontent.com/122522521/229350972-f4160fe4-f8a9-4091-9452-a7fed82a19b6.png)


Note that it is the final 6 digits of the URL.

8. Next, within DBT cloud, go to settings -> profile settings -> projects. Then, copy and paste the integers at the end of the URL. This is your account id and should be populated in your config.py as ```dbt_account_id``` .

9. On the same page, now click 'API Access'. If you already have an API key, copy it to your clipboard and paste it into config.py as ```dbt_api_key```. Otherwise, create a new API key and do the aforementioned steps.

10. Now, go to prefect cloud online at https://www.prefect.io/cloud/. If you have an account login, otherwise create an account.

11. Next, Create a workspace. To access DBT cloud and run your pipeline, you will need an API key to communicate with prefect cloud 2. To get this API key, click on your profile in the bottom left corner, and click the settings cog as shown in the image below:

![image](https://user-images.githubusercontent.com/122522521/229407825-05883f13-7b27-4696-b9e8-3489492b40ae.png)

12. Next, click the '+' icon to create a new api key, and call it what you want. Mine is prefect_crypto_api_key. Click create, and save this API key somewhere safe. This should also be added in config.py as ```prefect_cloud_api_key``` .

13. To login to prefect cloud locally, assuming you have installed prefect with ```pip install prefect``` and ```pip install prefect-cloud```, now you should run ```prefect cloud login```. This will ask you to login through either your browser or with an API key. Choose API key, and paste your API key into the command line. You should now get a prompt that says 'Authenticated with Prefect Cloud!'.

14. Name your ```prefect_cloud_dbt_block_name ``` within config.py. This can be any name. Mine was called 'DBT-creds'.

15. Ensure all variables within config.py have been filled appropriately. 

16. Ensure you have docker installed on your computer. If you are not sure run ```pip install docker```.

17. Now, navigate to the project directory, and run: ```docker build -t crypto_image .```.

18. Run the docker image with ```docker run -p 8000:8000 crypto_image```

19. This will run the entire ETL process. You will be able to see your run within prefect cloud, DBT (as a job that was run), and within both GCS and BQ as csv files, as well as tables will have been created.

## Dashboard
This is the final cryptocurrency dashboard:

![image](https://user-images.githubusercontent.com/122522521/228805080-97bf03ea-455b-4fbc-9d40-8a037db492f2.png)

![image](https://user-images.githubusercontent.com/122522521/228805282-5c85e734-cabc-4f27-b460-c155d24c5047.png)


**Additional Chart:**


![Cryptocurrency Volume Market Share (% USD)](https://user-images.githubusercontent.com/122522521/229414586-83639a84-d01e-4aff-9430-544419743a84.png)



Here is the link to my resultant cryptocurrency data dashboard:
https://docs.google.com/spreadsheets/d/1cO7mWZXv4BG1BCGUdTxBcyGvb9097Z04P4yzcj9QrDE/edit?usp=sharing

This was used as a proof of concept for a business idea. Unfortunately I cannot allow anyone to refresh this as it will cost money, so the drop down (which uses a parameter custom query) will not work (but rest assured, it does).

Contributors:

Lachlan Casey
