{{ config(materialized='table') }}

WITH artists_raw AS 
(
    SELECT 
        artist_id,
        artist_name,
        MAX(COALESCE(artist_popularity, 0)) AS artist_max_popularity,
        MAX(COALESCE(artist_followers_total, 0)) AS artist_followers_max_total,
        MIN(COALESCE(artist_popularity, 0)) AS artist_min_popularity,
        MIN(COALESCE(artist_followers_total, 0)) AS artist_followers_min_total,
        AVG(COALESCE(artist_popularity, 0)) AS artist_avg_popularity,
        AVG(COALESCE(artist_followers_total, 0)) AS artist_followers_avg_total,
        MAX(artist_insert_date) AS artist_last_update
    FROM {{ ref('stg_artists') }}
    GROUP BY artist_id, artist_name
), 
artists AS
(
    SELECT 
        artist_id,
        artist_name,
        artist_max_popularity,
        artist_followers_max_total,
        COALESCE({{ dbt_utils.safe_divide('artist_followers_max_total','artist_max_popularity') }}, 0) AS artist_max_followers_per_popularity,
        artist_min_popularity,
        artist_followers_min_total,
        COALESCE({{ dbt_utils.safe_divide('artist_followers_min_total','artist_min_popularity') }}, 0) AS artist_min_followers_per_popularity,
         artist_avg_popularity,
        artist_followers_avg_total,
        COALESCE({{ dbt_utils.safe_divide('artist_followers_avg_total','artist_avg_popularity') }}, 0) AS artist_avg_followers_per_popularity,
        artist_last_update
    FROM artists_raw
),
artists_genres AS 
(
    SELECT
        artist_id,
        COUNT(DISTINCT gender_name) AS count_genders,
        STRING_AGG(DISTINCT gender_name, ', ') AS list_genders
    FROM {{ ref('stg_artists_genres') }}
    GROUP BY artist_id
),
artists_images AS 
(
    SELECT
        artist_id,
        COUNT(DISTINCT image_url) AS count_images
    FROM {{ ref('stg_artists_images') }}
    GROUP BY artist_id
)
SELECT
    artists.artist_id,
    artists.artist_name,
    {{ get_popularity_category('artist_max_popularity') }} AS artist_max_popularity_category,
    artists.artist_max_popularity,
    artists.artist_followers_max_total,
    FORMAT('%.2f', artists.artist_max_followers_per_popularity) AS artist_max_followers_per_popularity,
    {{ get_popularity_category('artist_min_popularity') }} AS artist_min_popularity_category,
    artists.artist_min_popularity,
    artists.artist_followers_min_total,
    FORMAT('%.2f', artists.artist_min_followers_per_popularity) AS artist_min_followers_per_popularity,
    {{ get_popularity_category('artist_avg_popularity') }} AS artist_avg_popularity_category,    
    artists.artist_avg_popularity,
    artists.artist_followers_avg_total,
    FORMAT('%.2f', artists.artist_avg_followers_per_popularity) AS artist_avg_followers_per_popularity,
    COALESCE(artists_genres.count_genders, 0) AS artist_genres_count,
    COALESCE(artists_genres.list_genders, '') AS artist_genres,
    COALESCE(artists_images.count_images, 0) AS artist_images_count,
    artists.artist_last_update
FROM artists
LEFT JOIN artists_genres
ON artists.artist_id = artists_genres.artist_id
LEFT JOIN artists_images
ON artists.artist_id = artists_images.artist_id
