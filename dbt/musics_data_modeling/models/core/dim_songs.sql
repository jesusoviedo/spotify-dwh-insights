{{ config(materialized='table') }}

WITH songs AS 
(
    SELECT 
        song_id,
        song_name,
        song_duration_seconds,
        ROUND(song_duration_minutes, 0) AS song_duration_minutes,
        song_type,
        song_popularity,
        {{ is_column_true('song_is_explicit') }} AS song_is_explicit,
        {{ is_column_true('song_is_local') }} AS song_is_local,
        song_track_number_album,
        song_disc_number_album,
        song_insert_date,
        album_id,
        available_markets_id
    FROM {{ ref('stg_songs') }}
), 
available_markets AS 
(
    SELECT
        available_markets_id,
        COUNT(DISTINCT country_iso) AS count_country_iso,
        STRING_AGG(DISTINCT country_name, ', ') AS list_country
    FROM {{ ref('stg_available_markets') }}
    GROUP BY available_markets_id
),
artists AS 
(
    SELECT
        song_id,
        COUNT(DISTINCT artist_name) AS count_artist_name,
        STRING_AGG(DISTINCT artist_name, ', ') AS list_artist_name
    FROM {{ ref('stg_artists') }}
    GROUP BY song_id
),
albums AS 
(
    SELECT
        album_id,
        album_name,
        {{ is_popular('album_popularity') }} AS album_is_popular, 
        {{ get_popularity_category('album_popularity') }} AS album_popularity_category, 
        {{ get_album_recency_category('album_release_date_formatted') }} AS album_recency_category,
    FROM {{ ref('stg_albums') }}
)
SELECT
    songs.song_id,
    songs.song_name,
    {{ categorize_song_duration_seconds('song_duration_seconds') }} AS song_duration_category,
    {{ format_song_duration('song_duration_seconds') }} AS song_duration_time,
    songs.song_duration_minutes,
    songs.song_type,
    songs.song_popularity,
    {{ get_popularity_category('song_popularity') }} AS song_popularity_category, 
    {{ categorize_artists_count('count_artist_name') }} AS song_artist_category,
    COALESCE(artists.count_artist_name, 0) AS song_artist_count,
    COALESCE(artists.list_artist_name, '') AS song_artist,
    songs.song_is_explicit,
    songs.song_is_local,
    albums.album_id AS song_album_id,
    albums.album_name AS song_album_name,
    albums.album_is_popular AS song_album_is_popular,
    albums.album_popularity_category AS song_album_popularity_category,
    albums.album_recency_category AS song_album_recency_category,
    songs.song_track_number_album,
    songs.song_disc_number_album,
    COALESCE(available_markets.count_country_iso, 0) AS song_available_countries_count,
    COALESCE(available_markets.list_country, '') AS song_available_countries,
    songs.song_insert_date
FROM songs
LEFT JOIN available_markets
ON songs.available_markets_id = available_markets.available_markets_id
LEFT JOIN artists
ON songs.song_id = artists.song_id
LEFT JOIN albums
ON songs.album_id = albums.album_id
