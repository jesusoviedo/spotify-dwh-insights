{% macro categorize_song_duration(duration_column) %}
    CASE
        WHEN {{ duration_column }} < 150 THEN 'corta'  
        WHEN {{ duration_column }} >= 150 AND {{ duration_column }} < 240 THEN 'media'
        WHEN {{ duration_column }} >= 240 THEN 'larga'
        ELSE 'desconocida'
    END
{% endmacro %}
