{% macro format_song_duration(song_duration_seconds) %}
    FORMAT('%02d:%02d', 
        CAST(DIV(CAST({{ song_duration_seconds }} AS INT64), 60) AS INT64),
        CAST(MOD(CAST({{ song_duration_seconds }} AS INT64), 60) AS INT64)
    )
{% endmacro %}
