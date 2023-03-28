{% macro distinct_by_date(table) %}
SELECT 
date,
low as daily_price_low,
high as daily_price_high,
open as daily_price_open,
close as daily_price_close,
volume_from as crypto_volume,
volume_to as usd_volume
FROM (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY date ORDER BY date) as row_num
  FROM {{ table }}
) 
WHERE row_num = 1
{% endmacro %}