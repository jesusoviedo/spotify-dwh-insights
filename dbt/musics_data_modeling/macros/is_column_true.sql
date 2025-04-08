{% macro is_column_true(column) %}
    CASE 
        WHEN {{ column }} THEN 'si' 
        ELSE 'no'
    END
{% endmacro %}
