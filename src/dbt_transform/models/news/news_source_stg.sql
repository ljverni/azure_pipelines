
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/

WITH cte as (
    
    SELECT *, ROW_NUMBER() OVER (PARTITION BY source_id ORDER BY source_id DESC, date_extracted DESC) AS row_number
    FROM news.news_source_src    
)

SELECT
    source_id,
    name,
    url,
    description,
    language,
    country,
    date_extracted,
    batch_no
FROM cte
WHERE row_number = 1;

