{% macro get_album_length_category(column_name) %}
    CASE 
        WHEN {{ column_name }} <= 5 THEN 'mini album'
        WHEN {{ column_name }} BETWEEN 6 AND 12 THEN 'album breve'
        WHEN {{ column_name }} > 12 THEN 'album completo'
        ELSE 'desconocido'
    END
{% endmacro %}
