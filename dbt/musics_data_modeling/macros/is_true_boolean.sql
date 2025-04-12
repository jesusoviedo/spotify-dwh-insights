{% macro is_true_boolean(column_name) %}
    CASE WHEN {{ column_name }} = TRUE THEN 1 ELSE 0 END
{% endmacro %}