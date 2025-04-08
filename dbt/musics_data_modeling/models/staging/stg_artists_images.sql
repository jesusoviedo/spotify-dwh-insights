{{ config(
    materialized='view'
) }}


WITH artists_images AS 
(
    SELECT 
        cab._dlt_id,
        cab.id,
        det.url,
        det.height,
        det.width
    FROM {{ source('staging','songs__artists__images') }} AS cab
    LEFT JOIN {{ source('staging','songs__artists__images__images') }} AS det
    ON cab._dlt_id = det._dlt_parent_id
    WHERE det.url is not null

)
SELECT
    {{ dbt_utils.generate_surrogate_key(['_dlt_id']) }} AS image_id,
    url AS image_url,
    height AS image_height,
    width AS image_width,
    {{ dbt_utils.generate_surrogate_key(['id']) }} AS artist_id
FROM artists_images

-- dbt build --select <model_name> --vars '{'is_test': 'true'}'
{% if var('is_test', default=false) %}
  limit 100
{% endif %}


