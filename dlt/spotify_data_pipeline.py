import os
import shutil
import time
import argparse
import dlt
import requests
import fnmatch
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import numpy as np
from datetime import datetime, UTC
from google.cloud import storage
from dlt.sources.filesystem import filesystem


URI_TOKEN = "https://accounts.spotify.com/api/token"
URI_NEW_RELEASE = "https://api.spotify.com/v1/browse/new-releases"
URI_ALBUM_TRACKS = f"https://api.spotify.com/v1/albums"
CARPETA_TMP = "./tmp"
GCS_SUBFOLDER = "parquet"
LIMIT_SONGS = 1000


def params():
    parser = argparse.ArgumentParser(description='Carga de archivos usando DLT')
    parser.add_argument('--bucket_name', type=str, required=True, help='Nombre del bucket')
    parser.add_argument('--dataset_name', type=str, required=True, help='Nombre del Dataset')
    
    return parser.parse_args()


def obtener_token(client_id, client_secret):
    payload = {
        "grant_type": "client_credentials",
        "client_id": f"{client_id}",
        "client_secret": f"{client_secret}"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(URI_TOKEN, data=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    else:
        print(f"Error {response.status_code}: {response.json()}")


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
        print(f"Error {response.status_code}: {response.json()}")


def obtener_datos_albumes(list_lanzamiento):
    return [
        {
            'id': album["id"],
            'data_album': {
                "album_type": album["album_type"],
                "name": album["name"],
                "release_date": album["release_date"],
                "release_date_precision": album["release_date_precision"],
                "total_tracks": album["total_tracks"]
            }
        }
        for album in list_lanzamiento
    ]


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
        items = data.get("items")
        [item.update({"data_album": data_album}) for item in items]
        next_url = data.get("next")

        return items, next_url
    else:
        print(f"Error {response.status_code}: {response.json()}")


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
    client_id = os.getenv('CLIENTE_ID', None)
    client_secret = os.getenv('CLIENTE_SECRET', None)

    print(f"Obteniendo token -- fecha/hora:{datetime.now(UTC).isoformat()}")
    return obtener_token(client_id, client_secret)


def procesar_nuevos_lanzamientos(token):
    list_lanzamiento = []

    print(f"Procesando nuevos lanzamientos -- fecha/hora:{datetime.now(UTC).isoformat()}")
    items_0, next_url = obtener_nuevos_lanzamientos(token)
    list_lanzamiento.extend(items_0)  
    
    while next_url:
        items_n, next_url = obtener_nuevos_lanzamientos(token, next_url)
        list_lanzamiento.extend(items_n)

    return obtener_datos_albumes(list_lanzamiento)


def procesar_canciones_albumes(token, list_data_albumnes):
    parte = 1
    list_canciones = []
    list_filename = []

    print(f"Procesando canciones -- fecha/hora:{datetime.now(UTC).isoformat()}")
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

    source_file =  file_path.split("/")[-1]
    destination_blob_name = f"{GCS_SUBFOLDER}/{source_file}"
    client = storage.Client()

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)


def procesar_load_parquet_to_gcs(bucket_name, list_file_path):

    print(f"Subiendo archivos a GCS -- fecha/hora:{datetime.now(UTC).isoformat()}")
    for file_path in list_file_path:
        load_parquet_to_gcs(bucket_name, file_path)


def custom_serializer(record):
    for key, value in record.items():
        if isinstance(value, np.ndarray):
            record[key] = value.tolist()
    return record


def dlt_load_data_bigquery(bucket_name, dataset_name_dest):
    
    @dlt.resource(name="songs", primary_key="id", write_disposition="merge")
    def read_parquet_from_gcs(bucket_name):
        
        now = datetime.now()
        current_month = f"{now.month:02d}"
        current_year = str(now.year)
        prefix = f"{GCS_SUBFOLDER}/"
        patron = f"{prefix}songs_??{current_month}{current_year}_part*.parquet"

        client = storage.Client()
        bucket = client.bucket(bucket_name)

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
                    for record in df_chunk.to_dict(orient='records'):
                        yield custom_serializer(record)


    pipeline = dlt.pipeline(
        pipeline_name = "load_data_raw_bigquery",
        destination = "bigquery",
        dataset_name = dataset_name_dest,
        dev_mode = False
    )

    print(f"Cargando data raw en BigQuery -- fecha/hora:{datetime.now(UTC).isoformat()}")
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