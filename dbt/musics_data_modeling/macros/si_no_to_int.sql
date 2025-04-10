{% macro si_no_to_int(column_name) %}
    CASE WHEN {{ column_name }} = 'si' THEN 1 ELSE 0 END
{% endmacro %}