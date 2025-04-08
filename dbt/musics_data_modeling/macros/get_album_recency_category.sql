{% macro get_album_recency_category(column_name) %}
    CASE
        WHEN DATE_DIFF(CURRENT_DATE(), {{ column_name }}, YEAR) < 1 THEN 'reciente'
        WHEN DATE_DIFF(CURRENT_DATE(), {{ column_name }}, YEAR) BETWEEN 1 AND 10 THEN 'moderno'
        WHEN DATE_DIFF(CURRENT_DATE(), {{ column_name }}, YEAR) > 10 THEN 'clasico'
        ELSE 'desconocido'
    END
{% endmacro %}
