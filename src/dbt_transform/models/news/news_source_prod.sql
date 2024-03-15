
{{ 
    config(
        materialized='incremental',
        unique_key='source_id'
    )
}}


WITH cte AS (
    SELECT * FROM {{ ref('news_source_stg') }}
)

SELECT * FROM cte;
