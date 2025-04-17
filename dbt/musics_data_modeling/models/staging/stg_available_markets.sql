{{ config(
    materialized='view'
) }}

WITH available_markets AS
(
    SELECT 
        _dlt_parent_id,
        UPPER(value) AS country_iso,
        length(value) AS len_iso
    FROM {{ source('staging','songs__available_markets') }}
    WHERE value is not null
),
countries_descrip AS
(
    SELECT 
        country_name,
        iso_alpha_2
    FROM {{ ref('countries_iso') }}
    WHERE iso_alpha_2 is not null
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['_dlt_parent_id']) }} AS available_markets_id,
    available_markets.country_iso,
    COALESCE(LOWER(countries_descrip.country_name), 'n/a') AS country_name
FROM available_markets
LEFT JOIN countries_descrip
ON available_markets.country_iso = countries_descrip.iso_alpha_2
where len_iso = 2

-- dbt build --select <model_name> --vars '{'is_test': 'true'}'
{% if var('is_test', default=false) %}
  limit 100
{% endif %}
