{{ config(
    materialized='view'
) }}

WITH songs AS
(
    SELECT 
        *,
        ROW_NUMBER() OVER(PARTITION BY id, id_album) AS row_num
    FROM {{ source('staging','songs') }}
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['id']) }} AS song_id,
    UPPER(name) AS song_name,
    duration_ms AS song_duration_ms,
    duration_ms / 1000 AS song_duration_seconds,
    duration_ms / 60000.0 AS song_duration_minutes,
    LOWER(type) AS song_type,
    popularity AS song_popularity,
    explicit AS song_is_explicit,
    is_local AS song_is_local,
    track_number AS song_track_number_album,
    disc_number AS song_disc_number_album,
    PARSE_TIMESTAMP('%d/%m/%Y %H:%M:%S', insert_date) AS song_insert_date,
    {{ dbt_utils.generate_surrogate_key(['album__id']) }} AS album_id,
    {{ dbt_utils.generate_surrogate_key(['_dlt_id']) }} AS available_markets_id
FROM songs
WHERE row_num = 1

-- dbt build --select <model_name> --vars '{'is_test': 'true'}'
{% if var('is_test', default=false) %}
  limit 100
{% endif %}