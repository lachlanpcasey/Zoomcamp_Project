{{ config(materialized='table', schema='data_core') }}

with btc as (
    select *,
    'BTC' as crypto
    from {{ ref('stg_btc')}}
)
, eth as (
    select *,
    'ETH' as crypto
    from {{ ref('stg_eth')}}
)
, ens as (
    select *,
    'ENS' as crypto
    from {{ ref('stg_ens')}}
)
, ltc as (
    select *,
    'LTC' as crypto
    from {{ ref('stg_ltc')}}
)
, xrp as (
    select *,
    'XRP' as crypto
    from {{ ref('stg_xrp')}}
)

select 
    btc.date,
    btc.daily_price_open as btc_daily_price_open,
    xrp.daily_price_open as xrp_daily_price_open,
    eth.daily_price_open as eth_daily_price_open,
    ens.daily_price_open as ens_daily_price_open,
    ltc.daily_price_open as ltc_daily_price_open
from btc
left join eth on eth.date = btc.date
left join xrp on xrp.date = btc.date
left join ltc on ltc.date = btc.date
left join ens on ens.date = btc.date
