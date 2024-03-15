
/*
    Welcome to your first dbt model!
    Did you know that you can also configure models directly within SQL files?
    This will override configurations stated in dbt_project.yml

    Try changing "table" to "view" below
*/


with cte as (

    SELECT *, ROW_NUMBER() OVER (PARTITION BY article_id ORDER BY article_id DESC, date_extracted DESC) AS row_number
    FROM news.news_article_src
    WHERE date_extracted > (SELECT MAX(date_extracted) FROM news.news_article_prod)

)

SELECT
    article_id,
    title,
    link,
    content,
    publication_date,
    article_language,
    source_id,
    date_extracted,
    batch_no
FROM cte
WHERE row_number = 1;

/*
    Uncomment the line below to remove records with null `id` values
*/

-- where id is not null
