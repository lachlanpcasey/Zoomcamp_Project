{{ config(materialized='table', schema='data_core') }}

with btc as (
    select
        date,
        daily_price_low,
        daily_price_high,
        daily_price_open,
        daily_price_close,
        crypto_volume,
        usd_volume,
        'BTC' as crypto
    from {{ ref('stg_btc')}}
),
eth as (
    select
        date,
        daily_price_low,
        daily_price_high,
        daily_price_open,
        daily_price_close,
        crypto_volume,
        usd_volume,
        'ETH' as crypto
    from {{ ref('stg_eth')}}
),
ens as (
    select
        date,
        daily_price_low,
        daily_price_high,
        daily_price_open,
        daily_price_close,
        crypto_volume,
        usd_volume,
        'ENS' as crypto
    from {{ ref('stg_ens')}}
),
ltc as (
    select
        date,
        daily_price_low,
        daily_price_high,
        daily_price_open,
        daily_price_close,
        crypto_volume,
        usd_volume,
        'LTC' as crypto
    from {{ ref('stg_ltc')}}
),
xrp as (
    select
        date,
        daily_price_low,
        daily_price_high,
        daily_price_open,
        daily_price_close,
        crypto_volume,
        usd_volume,
        'XRP' as crypto
    from {{ ref('stg_xrp')}}
)

select 
    date,
    daily_price_low,
    daily_price_high,
    daily_price_open,
    daily_price_close,
    crypto_volume,
    usd_volume,
    crypto
from btc
union all
select 
    date,
    daily_price_low,
    daily_price_high,
    daily_price_open,
    daily_price_close,
    crypto_volume,
    usd_volume,
    crypto
from eth
union all
select 
    date,
    daily_price_low,
    daily_price_high,
    daily_price_open,
    daily_price_close,
    crypto_volume,
    usd_volume,
    crypto
from ens
union all
select 
    date,
    daily_price_low,
    daily_price_high,
    daily_price_open,
    daily_price_close,
    crypto_volume,
    usd_volume,
    crypto
from ltc
union all
select 
    date,
    daily_price_low,
    daily_price_high,
    daily_price_open,
    daily_price_close,
    crypto_volume,
    usd_volume,
    crypto
from xrp
