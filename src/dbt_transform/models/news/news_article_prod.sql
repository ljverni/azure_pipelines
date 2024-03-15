
{{
    config(
        materialized='incremental',
        unique_key='article_id'
    )
}}

WITH cte AS (

    SELECT * FROM {{ ref('news_article_stg') }}

)

SELECT * FROM cte;
