{{ config(materialized='table') }}

WITH stg_artists AS 
(
    SELECT 
        artist_id,
        song_id
    FROM {{ ref('stg_artists') }}
), 
songs_by_artist_album AS (
    SELECT
        stg_artists.artist_id AS song_artist_id,
        songs.song_album_id,
        songs.song_id,
        songs.song_name,
        songs.song_duration_minutes,
        songs.song_popularity,
        songs.song_is_explicit,
        songs.song_available_countries_count
    FROM {{ ref('dim_songs') }} AS songs
    INNER JOIN stg_artists
    ON songs.song_id = stg_artists.song_id
),
albums AS (
    SELECT
        album_id,
        album_name,
        album_type,
        album_release_year,
        album_popularity,
        album_popularity_category,
        album_length_category,
        album_avg_song_duration
    FROM {{ ref('dim_albums') }}
),
artists AS (
    SELECT
        artist_id,
        artist_name,
        artist_avg_popularity,
        artist_avg_popularity_category,
        artist_genres,
        artist_genres_count,
        artist_images_count
    FROM {{ ref('dim_artists') }}
),
artists_albums_songs AS (
    SELECT
        artist.artist_id,
        artist.artist_name,
        artist.artist_avg_popularity,
        artist.artist_avg_popularity_category,
        artist.artist_genres,
        artist.artist_genres_count,
        artist.artist_images_count,
        album.album_id,
        album.album_name,
        album.album_type,
        album.album_release_year,
        album.album_popularity,
        album.album_popularity_category,
        album.album_length_category,
        album.album_avg_song_duration,
        COUNT(songs_artist_album.song_id) AS total_songs,
        SUM({{ si_no_to_int('song_is_explicit') }}) AS total_explicit_songs,
        ROUND(AVG(songs_artist_album.song_duration_minutes), 2) AS avg_song_duration,
        ROUND(AVG(songs_artist_album.song_popularity), 2) AS avg_song_popularity,
    FROM songs_by_artist_album AS songs_artist_album
    JOIN albums AS album  ON songs_artist_album.song_album_id = album.album_id
    JOIN artists AS artist ON songs_artist_album.song_artist_id = artist.artist_id
    GROUP BY 
        artist.artist_id, artist.artist_name, artist.artist_avg_popularity, artist.artist_avg_popularity_category,
        artist.artist_genres, artist.artist_genres_count, artist.artist_images_count,
        album.album_id, album.album_name, album.album_type, album.album_release_year,
        album.album_popularity, album.album_popularity_category, album.album_length_category, album.album_avg_song_duration
)
SELECT
    artist_id,
    artist_name,
    artist_avg_popularity,
    artist_avg_popularity_category,
    artist_genres,
    artist_genres_count,
    artist_images_count,
    album_id,
    album_name,
    album_type,
    album_release_year,
    album_popularity,
    album_popularity_category,
    album_length_category,
    album_avg_song_duration,
    total_songs,
    total_explicit_songs,
    avg_song_duration,
    {{ categorize_song_duration_minutes('avg_song_duration') }} AS avg_song_duration_category,
    avg_song_popularity,
    {{ get_popularity_category('avg_song_popularity') }} AS avg_song_popularity_category
FROM artists_albums_songs
