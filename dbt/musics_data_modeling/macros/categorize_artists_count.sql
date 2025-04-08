-- macros/categorize_artists_count.sql
{% macro categorize_artists_count(column_name) %}
    CASE 
        WHEN {{ column_name }} = 1 THEN 'solista'
        WHEN {{ column_name }} = 2 THEN 'duo'
        WHEN {{ column_name }} = 3 THEN 'trio'
        WHEN {{ column_name }} >= 4 THEN 'colaboracion multiple'
        ELSE 'desconocido'
    END
{% endmacro %}
