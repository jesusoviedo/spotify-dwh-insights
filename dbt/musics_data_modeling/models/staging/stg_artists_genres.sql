{{ config(
    materialized='view'
) }}

WITH artists_genres AS
(
    SELECT 
        cab._dlt_id,
        cab.id,
        det.value
    FROM {{ source('staging','songs__artists__genres') }} AS cab
    LEFT JOIN {{ source('staging','songs__artists__genres__genres') }} AS det
    ON cab._dlt_id = det._dlt_parent_id
    WHERE det.value is not null
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['_dlt_id']) }} AS gender_id,
    LOWER(value) AS gender_name,
    {{ dbt_utils.generate_surrogate_key(['id']) }} AS artist_id
FROM artists_genres

-- dbt build --select <model_name> --vars '{'is_test': 'true'}'
{% if var('is_test', default=false) %}
  limit 100
{% endif %}
