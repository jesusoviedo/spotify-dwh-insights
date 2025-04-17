{{ config(
    materialized='view'
) }}

WITH artists AS
(
    SELECT 
        *,
        ROW_NUMBER() OVER(PARTITION BY id, id_song) AS row_num
    FROM {{ source('staging','songs__artists') }}
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['id']) }} AS artist_id,
    UPPER(name) AS artist_name,
    popularity AS artist_popularity,
    followers__total AS artist_followers_total,
    PARSE_TIMESTAMP('%d/%m/%Y %H:%M:%S', insert_date) AS artist_insert_date,
    {{ dbt_utils.generate_surrogate_key(['id_song']) }} AS song_id
FROM artists
WHERE row_num = 1

-- dbt build --select <model_name> --vars '{'is_test': 'true'}'
{% if var('is_test', default=false) %}
  limit 100
{% endif %}
