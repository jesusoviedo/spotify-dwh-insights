{% macro is_popular(column) %}
    CASE 
        WHEN {{ column }} > 70 THEN 'si' 
        ELSE 'no'
    END
{% endmacro %}
