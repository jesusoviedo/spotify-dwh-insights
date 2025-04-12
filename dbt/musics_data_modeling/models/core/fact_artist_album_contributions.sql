{{ config(materialized='table') }}


WITH artists AS 
(
    SELECT 
        artist_id,
        song_id
    FROM {{ ref('stg_artists') }}
), 
songs AS 
(
    SELECT 
        song_id,
        song_album_id AS album_id
    FROM {{ ref('dim_songs') }}
), 
album_artists AS 
(
    SELECT 
        artists.artist_id,
        songs.album_id,
        COUNT(DISTINCT songs.song_id) AS total_songs_by_artist_in_album,
        COUNT(DISTINCT artists.artist_id) OVER(PARTITION BY songs.album_id) AS total_artists_in_album
    FROM artists
    INNER JOIN songs
    ON artists.song_id = songs.song_id
    GROUP BY artists.artist_id, songs.album_id
),
dim_albums AS 
(
    SELECT
        album_id,
        album_name,
        album_release_date,
        album_release_year,
        album_popularity,
        album_is_popular,
        album_popularity_category,
        album_total_tracks,
        album_total_song_explicit,
        album_avg_song_duration
    FROM {{ ref('dim_albums') }}
),
dim_artists AS 
(
    SELECT
        artist_id,
        artist_name,
        artist_max_popularity,
        artist_max_popularity_category,
        artist_genres_count,
        artist_genres,
        artist_images_count
    FROM {{ ref('dim_artists') }}
)
SELECT
    dim_albums.album_id,
    dim_albums.album_name,
    dim_albums.album_release_year,
    dim_albums.album_release_date,
    dim_albums.album_popularity,
    dim_albums.album_is_popular,
    dim_albums.album_popularity_category,
    dim_albums.album_total_tracks,
    dim_albums.album_total_song_explicit,
    dim_albums.album_avg_song_duration,
    dim_artists.artist_id,
    dim_artists.artist_name,
    dim_artists.artist_max_popularity,
    dim_artists.artist_max_popularity_category,
    dim_artists.artist_genres_count,
    dim_artists.artist_genres,
    dim_artists.artist_images_count,
    album_artists.total_songs_by_artist_in_album AS artist_album_song_count,   
    COALESCE(ROUND(100 * album_artists.total_songs_by_artist_in_album / NULLIF(dim_albums.album_total_tracks, 0), 2), 0) AS artist_album_song_percent,
    CASE 
        WHEN total_artists_in_album = 1
        THEN 'si' ELSE 'no' 
    END AS is_only_artist_on_album 
FROM dim_albums
INNER JOIN album_artists
ON dim_albums.album_id = album_artists.album_id
INNER JOIN dim_artists
ON album_artists.artist_id = dim_artists.artist_id






