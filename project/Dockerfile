FROM python:3.9.13-slim-buster

RUN pip install prefect-dbt google-cloud google-cloud-core pandas google-cloud-bigquery google-cloud-storage

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

COPY ./prefect_crypto_flow.py /app
COPY ./Crypto_data_gcs_to_bq.py /app
COPY ./Crypto_data_ingest.py /app
COPY ./config.py /app
COPY ./creds.json /app


EXPOSE 8000

CMD ["python", "./prefect_crypto_flow.py"]
