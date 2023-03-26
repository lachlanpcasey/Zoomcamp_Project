{% macro distinct_by_date(table) %}
SELECT *
FROM (
  SELECT *,
    ROW_NUMBER() OVER (PARTITION BY date ORDER BY date) as row_num
  FROM {{ table }}
) 
WHERE row_num = 1
{% endmacro %}