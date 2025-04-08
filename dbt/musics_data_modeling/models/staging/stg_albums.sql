{{ config(
    materialized='view'
) }}

WITH albums AS 
(
    SELECT *,
         ROW_NUMBER() OVER(PARTITION BY album__id) AS row_num
    FROM {{ source('staging','songs') }}
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['album__id']) }} AS album_id,
    UPPER(album__name) AS album_name,
    LOWER(album__album_type) AS album_type,
    album__popularity AS album_popularity,
    album__release_date AS album_release_date,
    LOWER(album__release_date_precision) AS album_release_date_precision,
    CASE 
        WHEN album__release_date_precision = 'year' THEN PARSE_DATE('%Y-%m-%d', album__release_date || '-01-01')
        WHEN album__release_date_precision = 'month' THEN PARSE_DATE('%Y-%m-%d', album__release_date || '-01')
        WHEN album__release_date_precision = 'day' THEN PARSE_DATE('%Y-%m-%d', album__release_date)
        ELSE NULL
    END AS album_release_date_formatted,    
    album__total_tracks AS album_total_tracks,
    LOWER(album__label) AS album_label,
    PARSE_TIMESTAMP('%d/%m/%Y %H:%M:%S', album__insert_date) AS album_insert_date
FROM albums
WHERE row_num = 1

-- dbt build --select <model_name> --vars '{'is_test': 'true'}'
{% if var('is_test', default=false) %}
  limit 100
{% endif %}