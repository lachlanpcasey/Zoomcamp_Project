{{ config(materialized='view', schema='data_staging') }}

{{ distinct_by_date(source('staging', 'ENS_*')) }}