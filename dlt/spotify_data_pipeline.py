import argparse
import fnmatch
import os
import shutil
from datetime import datetime

import numpy
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytz
import requests
import requests_cache
from google.cloud import storage

import dlt

URI_TOKEN = "https://accounts.spotify.com/api/token"
URI_NEW_RELEASE = "https://api.spotify.com/v1/browse/new-releases"
URI_ALBUM_TRACKS = "https://api.spotify.com/v1/albums"
URI_TRACKS = "https://api.spotify.com/v1/tracks"
URI_ARTISTS = "https://api.spotify.com/v1/artists"
CARPETA_TMP = "./tmp"
GCS_SUBFOLDER = "parquet"
LIMIT_SONGS = 1000
CACHE_PATH = "../spotify_cache.sqlite"
UTC_MINUS_3 = pytz.timezone("America/Asuncion")
DATE_NOW = datetime.now(UTC_MINUS_3).strftime("%d/%m/%Y %H:%M:%S")


def only_cache_success(response):
    return response.status_code == 200


requests_cache.install_cache(
    CACHE_PATH,
    backend="sqlite",
    expire_after=12 * 60 * 60,
    filter_fn=only_cache_success,
)


def params():
    parser = argparse.ArgumentParser(description="Carga de archivos usando DLT")
    parser.add_argument("--bucket_name", type=str, required=True, help="Nombre del bucket")
    parser.add_argument("--dataset_name", type=str, required=True, help="Nombre del Dataset")

    return parser.parse_args()


def obtener_token(client_id, client_secret):

    with requests_cache.disabled():
        payload = {
            "grant_type": "client_credentials",
            "client_id": f"{client_id}",
            "client_secret": f"{client_secret}",
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(URI_TOKEN, data=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            print(f"Error {response.status_code}: {response.text}")


def obtener_nuevos_lanzamientos(token, url=URI_NEW_RELEASE):

    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": 20, "offset": 0}

    if "?" in url:
        params["limit"] = url.split("?")[1].split("&")[1].split("=")[1]
        params["offset"] = url.split("?")[1].split("&")[0].split("=")[1]

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        items = data.get("albums", {}).get("items")
        next_url = data.get("albums", {}).get("next")

        return items, next_url
    else:
        print(f"Error {response.status_code}: {response.text}")


def obtener_album(token, id_album):

    url = f"{URI_ALBUM_TRACKS}/{id_album}"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        return data
    else:
        print(f"Error {response.status_code}: {response.text}")


def transformar_datos_albumes(list_lanzamiento, token):

    albums = [obtener_album(token, lanzamiento["id"]) for lanzamiento in list_lanzamiento]
    transformed_albums = [
        {
            "id": album["id"],
            "data_album": {
                "id": album["id"],
                "album_type": album["album_type"],
                "name": album["name"],
                "release_date": album["release_date"],
                "release_date_precision": album["release_date_precision"],
                "total_tracks": album["total_tracks"],
                "popularity": album["popularity"],
                "label": album["label"],
                "insert_date": DATE_NOW,
            },
        }
        for album in albums
    ]
    return transformed_albums


def transformar_datos_artistas(list_artists, id_song):

    transformed_artists = [
        {
            "external_urls": artists["external_urls"],
            "followers": artists["followers"],
            "genres": [{"id": artists["id"], "genres": artists["genres"]}],
            "href": artists["href"],
            "id": artists["id"],
            "images": [{"id": artists["id"], "images": artists["images"]}],
            "name": artists["name"],
            "popularity": artists["popularity"],
            "type": artists["type"],
            "uri": artists["uri"],
            "id_song": id_song,
            "insert_date": DATE_NOW,
        }
        for artists in list_artists
    ]
    return transformed_artists


def obtener_artistas(token, dic_list_artista):

    url = URI_ARTISTS
    list_id_artists = dic_list_artista.get("list_id_artist")
    id_song = dic_list_artista.get("id_song")

    headers = {"Authorization": f"Bearer {token}"}
    params = {"ids": ",".join(list_id_artists)}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        items = data.get("artists")

        return transformar_datos_artistas(items, id_song)
    else:
        print(f"Error {response.status_code}: {response.text}")


def transformar_datos_canciones(list_canciones):

    transformed_canciones = {cancion["id"]: cancion["popularity"] for cancion in list_canciones}
    return transformed_canciones


def obtener_popularidad_canciones(token, list_id_cancion):

    url = URI_TRACKS

    headers = {"Authorization": f"Bearer {token}"}
    params = {"ids": ",".join(list_id_cancion)}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        items = data.get("tracks")

        return transformar_datos_canciones(items)
    else:
        print(f"Error {response.status_code}: {response.text}")


def obtener_canciones_albumes(token, id_album, data_album, url=None):

    url = url if url else f"{URI_ALBUM_TRACKS}/{id_album}/tracks"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": 20, "offset": 0}

    if "?" in url:
        params["limit"] = url.split("?")[1].split("&")[1].split("=")[1]
        params["offset"] = url.split("?")[1].split("&")[0].split("=")[1]

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])

        list_id_canciones = [item.get("id") for item in items]
        dict_pop_canciones = obtener_popularidad_canciones(token, list_id_canciones)

        for item in items:

            id_cancion = item.get("id")
            artists_list = item.get("artists", [])
            list_id_artist = [artist.get("id") for artist in artists_list]
            dic_list_artista = {"id_song": id_cancion, "list_id_artist": list_id_artist}
            artistas = obtener_artistas(token, dic_list_artista)

            item.update(
                {
                    "popularity": dict_pop_canciones.get(id_cancion),
                    "id_album": id_album,
                    "album": data_album,
                    "artists": artistas,
                    "insert_date": DATE_NOW,
                }
            )

        next_url = data.get("next")

        return items, next_url
    else:
        print(f"Error {response.status_code}: {response.text}")


def guardar_parquet(canciones, parte):
    fecha_actual = datetime.now().strftime("%d%m%Y")
    os.makedirs(CARPETA_TMP, exist_ok=True)
    filename = os.path.join(CARPETA_TMP, f"songs_{fecha_actual}_part{parte}.parquet")

    df = pd.DataFrame(canciones)
    table = pa.Table.from_pandas(df)
    pq.write_table(table, filename)

    return filename


def eliminar_carpeta_tmp():

    if os.path.exists(CARPETA_TMP):
        shutil.rmtree(CARPETA_TMP)
        print(f"Carpeta '{CARPETA_TMP}' eliminada con éxito.")
    else:
        print(f"La carpeta '{CARPETA_TMP}' no existe.")


def procesar_token():
    client_id = os.getenv("CLIENTE_ID", None)
    client_secret = os.getenv("CLIENTE_SECRET", None)

    print(f"Obteniendo token -- fecha/hora:{datetime.now(UTC_MINUS_3).isoformat()}")
    return obtener_token(client_id, client_secret)


def procesar_nuevos_lanzamientos(token):
    list_lanzamiento = []

    print(f"Procesando nuevos lanzamientos -- fecha/hora:{datetime.now(UTC_MINUS_3).isoformat()}")
    items_0, next_url = obtener_nuevos_lanzamientos(token)
    list_lanzamiento.extend(items_0)

    while next_url:
        items_n, next_url = obtener_nuevos_lanzamientos(token, next_url)
        list_lanzamiento.extend(items_n)

    return transformar_datos_albumes(list_lanzamiento, token)


def procesar_canciones_albumes(token, list_data_albumnes):
    parte = 1
    list_canciones = []
    list_filename = []

    print(f"Procesando canciones -- fecha/hora:{datetime.now(UTC_MINUS_3).isoformat()}")
    for dic_album in list_data_albumnes:
        id_album = dic_album.get("id")
        data_album = dic_album.get("data_album")
        items_0, next_url = obtener_canciones_albumes(token, id_album, data_album)
        list_canciones.extend(items_0)

        while next_url:
            items_n, next_url = obtener_canciones_albumes(token, id_album, data_album, next_url)
            list_canciones.extend(items_n)

        if len(list_canciones) >= LIMIT_SONGS:
            filename = guardar_parquet(list_canciones[:LIMIT_SONGS], parte)
            list_filename.append(filename)
            list_canciones = list_canciones[LIMIT_SONGS:]
            parte += 1

    if list_canciones:
        filename = guardar_parquet(list_canciones, parte)
        list_filename.append(filename)

    return list_filename


def load_parquet_to_gcs(bucket_name, file_path):

    source_file = file_path.split("/")[-1]
    destination_blob_name = f"{GCS_SUBFOLDER}/{source_file}"
    client = storage.Client()

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)


def procesar_load_parquet_to_gcs(bucket_name, list_file_path):

    print(f"Subiendo archivos a GCS -- fecha/hora:{datetime.now(UTC_MINUS_3).isoformat()}")
    for file_path in list_file_path:
        load_parquet_to_gcs(bucket_name, file_path)


def custom_serializer(value):
    if isinstance(value, numpy.ndarray):
        if value.size == 0:
            return []
        lista_value = value.tolist()
        return [custom_serializer(v) for v in lista_value]
    elif isinstance(value, dict):
        return {k: custom_serializer(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [custom_serializer(v) for v in value]
    elif isinstance(value, (str, int, bool, float)) or value is None:
        return value
    else:
        print(f"Tipo no compatible encontrado: {type(value)} - {value}")
        return str(value)


def dlt_load_data_bigquery(bucket_name, dataset_name_dest):

    @dlt.resource(name="songs", primary_key=("id", "id_album"), write_disposition="merge")
    def read_parquet_from_gcs(bucket_name):

        now = datetime.now()
        current_month = f"{now.month:02d}"
        current_year = str(now.year)
        prefix = f"{GCS_SUBFOLDER}/"
        patron = f"{prefix}songs_??{current_month}{current_year}_part*.parquet"

        client = storage.Client()

        os.makedirs(CARPETA_TMP, exist_ok=True)
        blobs = client.list_blobs(bucket_name, prefix=prefix)

        for blob in blobs:
            if fnmatch.fnmatch(blob.name, patron):
                file_path = os.path.join(CARPETA_TMP, os.path.basename(blob.name))
                blob.download_to_filename(file_path)

                parquet_file = pq.ParquetFile(file_path)
                chunk_size = int(LIMIT_SONGS / 4)

                for batch in parquet_file.iter_batches(batch_size=chunk_size):
                    df_chunk = batch.to_pandas()
                    for record in df_chunk.to_dict(orient="records"):
                        yield custom_serializer(record)

    pipeline = dlt.pipeline(
        pipeline_name="load_data_raw_bigquery",
        destination="bigquery",
        dataset_name=dataset_name_dest,
        dev_mode=False,
    )

    print(f"Cargando data raw en BigQuery -- fecha/hora:{datetime.now(UTC_MINUS_3).isoformat()}")
    load_info = pipeline.run(read_parquet_from_gcs(bucket_name))
    print(load_info)


def main():

    args = params()
    bucket_name = args.bucket_name
    dataset_name = args.dataset_name
    token = procesar_token()

    if token:
        list_data_albumnes = procesar_nuevos_lanzamientos(token)

    if list_data_albumnes:
        list_file_path = procesar_canciones_albumes(token, list_data_albumnes)

        procesar_load_parquet_to_gcs(bucket_name, list_file_path)
        eliminar_carpeta_tmp()

        dlt_load_data_bigquery(bucket_name, dataset_name)
        eliminar_carpeta_tmp()


if __name__ == "__main__":
    main()
