{% macro get_popularity_category(popularity_value) %}
    case
        when {{ popularity_value }} between 0 and 39 then 'baja'
        when {{ popularity_value }} between 40 and 69 then 'moderada'
        when {{ popularity_value }} between 70 and 89 then 'alta'
        when {{ popularity_value }} between 90 and 100 then 'muy alta'
        else 'desconocida'
    end
{% endmacro %}
