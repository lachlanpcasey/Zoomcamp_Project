import requests
import json
import csv
from google.cloud import storage
import pandas as pd
import os
from datetime import datetime
import sys
from config import cryptocompare_api_key, gcs_bucket_name, creds


# get the crypto argument passed to the script
crypto = sys.argv[1]

current_date = datetime.now().date()
current_date_str = current_date.strftime('%Y-%m-%d')
api_key = cryptocompare_api_key
cryptocurrencies = [crypto]
url = 'https://min-api.cryptocompare.com/data/v2/histoday'
params = {'fsym': ','.join(cryptocurrencies), 'tsym': 'USD', 'limit': 2000,'api_key': api_key}
headers = {'Accept': 'application/json'}
response = requests.get(url, params=params, headers=headers)
data = json.loads(response.text)["Data"]["Data"]
daily_data = {}
for day in data:
    date = day["time"]
    daily_data[date] = {
        "open": day["open"],
        "close": day["close"],
        "high": day["high"],
        "low": day["low"],
        "volume_from": day["volumefrom"],
        "volume_to": day["volumeto"]
    }
daily_list = []
for date, values in daily_data.items():
    daily_dict = {"date": date}
    daily_dict.update(values)
    daily_list.append(daily_dict)
df = pd.DataFrame(daily_list)
df['date'] = pd.to_datetime(df['date'], unit='s').dt.date
client = storage.Client.from_service_account_json(creds)
bucket = client.bucket(gcs_bucket_name)
if not os.path.exists('crypto_data'):
    os.makedirs('crypto_data')
crypto_folder = f'crypto_data/{crypto}'
if not os.path.exists(crypto_folder):
    os.makedirs(crypto_folder)
file_name = f"{crypto}_{current_date}.csv"
blob = bucket.blob(f"crypto_data/{crypto}/{file_name}")
if blob.exists():
    print(f"{file_name} already exists in the bucket")
else:
    df.to_csv(f"{crypto_folder}/{file_name}", index=False)
    blob.upload_from_filename(f"{crypto_folder}/{file_name}", content_type="text/csv")
    print(f"{file_name} uploaded to the bucket")
