{{ config(materialized='table', schema='data_core', clustering = ['date']) }}

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
    btc.usd_volume as btc_usd_volume,
    xrp.usd_volume as xrp_usd_volume,
    eth.usd_volume as eth_usd_volume,
    ens.usd_volume as ens_usd_volume,
    ltc.usd_volume as ltc_usd_volume
from btc
left join eth on eth.date = btc.date
left join xrp on xrp.date = btc.date
left join ltc on ltc.date = btc.date
left join ens on ens.date = btc.date
