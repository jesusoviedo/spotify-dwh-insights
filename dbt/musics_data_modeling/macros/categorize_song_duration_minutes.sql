{% macro categorize_song_duration_minutes(duration_column) %}
    CASE
        WHEN {{ duration_column }} < 2.5 THEN 'corta'  
        WHEN {{ duration_column }} >= 2.5 AND {{ duration_column }} < 4 THEN 'media'
        WHEN {{ duration_column }} >= 4 THEN 'larga'
        ELSE 'desconocida'
    END
{% endmacro %}
