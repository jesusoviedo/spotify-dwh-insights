{% test check_negative_values(model, column_name) %}
    SELECT
        {{ column_name }} 
    FROM
        {{ model }}
    WHERE
        CAST({{ column_name }} AS FLOAT64)  < 0
    LIMIT 1
{% endtest  %}