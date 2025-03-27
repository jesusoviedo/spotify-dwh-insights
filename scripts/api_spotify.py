import os
import shutil
import time
import requests
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa

from datetime import datetime, UTC


URI_TOKEN = "https://accounts.spotify.com/api/token"
URI_NEW_RELEASE = "https://api.spotify.com/v1/browse/new-releases"
URI_ALBUM_TRACKS = f"https://api.spotify.com/v1/albums"
CARPETA_TMP = "./tmp"

def optener_token(client_id, client_secret):
    payload = {
        "grant_type": "client_credentials",
        "client_id": f"{client_id}",
        "client_secret": f"{client_secret}"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(URI_TOKEN, data=payload, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"Token generado correctamente en fecha/hora:{datetime.now(UTC).isoformat()}")
        return data.get("access_token")
    else:
        print(f"Error {response.status_code}: {response.json()}")


def optener_nuevos_lanzamientos(token, url=URI_NEW_RELEASE):

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

        print(f"Nuevos lanzamientos obtenidos correctamente en fecha/hora:{datetime.now(UTC).isoformat()} - cantidad: {len(items)}")
        return items, next_url
    else:
        print(f"Error {response.status_code}: {response.json()}")


def optener_datos_albumes(list_lanzamiento):

    return [{"id" : lanzamiento.get("id"), "release_date" : lanzamiento.get("release_date")} for lanzamiento in list_lanzamiento]


def optener_canciones_albumes(token, id_album, url=None):

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
        next_url = data.get("next")

        print(f"Canciones obtenidos correctamente, en fecha/hora:{datetime.now(UTC).isoformat()} - cantidad: {len(items)}")
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

    print(f"Guardado: {filename}")


def eliminar_carpeta_tmp():

    if os.path.exists(CARPETA_TMP):
        shutil.rmtree(CARPETA_TMP)
        print(f"Carpeta '{CARPETA_TMP}' eliminada con éxito.")
    else:
        print(f"La carpeta '{CARPETA_TMP}' no existe.")


def main():
    client_id = os.getenv('CLIENTE_ID', None)
    client_secret = os.getenv('CLIENTE_SECRET', None)
    token = optener_token(client_id, client_secret)


    list_lanzamiento = []
    items_0, next_url = optener_nuevos_lanzamientos(token)
    list_lanzamiento.extend(items_0)  
    
    while next_url:
        items_n, next_url = optener_nuevos_lanzamientos(token, next_url)
        list_lanzamiento.extend(items_n)


    list_id_albumnes = optener_datos_albumes(list_lanzamiento)
    parte = 1
    list_canciones = []
    for dic_album in list_id_albumnes:
        id_album = dic_album.get("id")
        items_0, next_url = optener_canciones_albumes(token, id_album)
        list_canciones.extend(items_0)  

        while next_url:
            items_n, next_url = optener_canciones_albumes(token, id_album, next_url)
            list_canciones.extend(items_n)

        if len(list_canciones) >= 500:
            guardar_parquet(list_canciones[:500], parte)
            list_canciones = list_canciones[500:]
            parte += 1

    if list_canciones:
        guardar_parquet(list_canciones, parte)


if __name__ == "__main__":
    main()