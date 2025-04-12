{{ config(materialized='table') }}

WITH albums AS 
(
    SELECT 
        album_id,
        album_name,
        album_type,
        album_popularity,
        album_release_date,
        album_release_date_precision,
        album_release_date_formatted,
        EXTRACT(YEAR FROM album_release_date_formatted) AS album_release_year,
        album_total_tracks,
        album_label,
        album_insert_date
    FROM {{ ref('stg_albums') }}
), 
songs AS 
(
    SELECT
        album_id,
        ROUND(MAX(song_duration_minutes), 2) AS song_max_duration_minutes,
        ROUND(MIN(song_duration_minutes), 2) AS song_min_duration_minutes,
        ROUND(AVG(song_duration_minutes), 2) AS song_avg_duration_minutes,
        SUM({{ is_true_boolean('song_is_explicit') }}) AS song_total_explicit
    FROM {{ ref('stg_songs') }}
    GROUP BY album_id
)
SELECT
    albums.album_id,
    albums.album_name,
    albums.album_type,
    {{ is_popular('album_popularity') }} AS album_is_popular, 
    albums.album_popularity,
    {{ get_popularity_category('album_popularity') }} AS album_popularity_category, 
    albums.album_release_date_formatted AS album_release_date,
    albums.album_release_date_precision,
    albums.album_release_year,
    {{ get_album_recency_category('album_release_date_formatted') }} AS album_recency_category, 
    albums.album_total_tracks,
    {{ get_album_length_category('album_total_tracks') }} AS album_length_category,
    albums.album_label,
    FORMAT('%.2f', songs.song_max_duration_minutes) AS album_max_song_duration,
    FORMAT('%.2f', songs.song_min_duration_minutes) AS album_min_song_duration,
    FORMAT('%.2f', songs.song_avg_duration_minutes) AS album_avg_song_duration,
    songs.song_total_explicit AS album_total_song_explicit,
    albums.album_insert_date
FROM albums
LEFT JOIN songs
ON albums.album_id = songs.album_id
