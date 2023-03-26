{{
  config(
    materialized='view',
    schema='crypto_data_staging'
  )
}}

SELECT *
FROM (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY date ORDER BY date) as row_num
  FROM {{ source('staging', 'BTC_*') }}
) 
WHERE row_num = 1