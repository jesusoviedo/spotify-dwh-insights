# 📊 Entendiendo los Datos

Este proyecto utiliza la API de Spotify para obtener información sobre nuevos lanzamientos y sus canciones. A continuación, se describe el flujo de obtención de datos y los servicios involucrados.



## 📌 1. Obtención del token de acceso
🔗 [Documentación Oficial](https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow)

Antes de acceder a cualquier otro servicio, es necesario autenticar la aplicación mediante el flujo de Client Credentials.

### Solicitud del Token

#### 📤 **Método:** `POST`

#### 🔗 **Endpoint:** `https://accounts.spotify.com/api/token`

#### 📄 **Parámetros:**
- `grant_type`: `"client_credentials"`
- `client_id`: tu Client ID de Spotify
- `client_secret`: tu Client Secret de Spotify

#### 📥 **Respuesta esperada (JSON - Ejemplo):**

```json
{
  "access_token": "BQC...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

El `access_token` obtenido se usará en las siguientes llamadas a la API.



## 🎶 2. Obtención de nuevos lanzamientos
🔗 [Documentación Oficial](https://developer.spotify.com/documentation/web-api/reference/get-new-releases)

Este servicio obtiene una lista de álbumes recientemente publicados en Spotify.

### Solicitud de nuevos lanzamientos

#### 📤 **Método:** `GET`
#### 🔗 **Endpoint:** `https://api.spotify.com/v1/browse/new-releases`

#### 📄 **Parámetros opcionales:**
- `limit`: cantidad de álbumes a recuperar (Ejemplo: `10`)
- `offset`: paginación

#### 📥 **Respuesta esperada (JSON - Ejemplo):**

```json
{
  "albums": {
    "items": [
      {
        "id": "12345",
        "name": "Nuevo Álbum",
        "artists": [{"name": "Artista X"}],
        "release_date": "2025-03-26"
      }
    ]
    ....
  }
}
```

📂 **Para ver una respuesta completa, consulta el archivo:** [`example_new_releases.json`](./example_new_releases.json)

Cada álbum tiene un `id`, que se usará en el siguiente servicio para obtener sus canciones.



## 🎵 3. Obtención de canciones de un álbum
🔗 [Documentación Oficial](https://developer.spotify.com/documentation/web-api/reference/get-an-albums-tracks)

Este servicio permite obtener todas las canciones de un álbum específico.

### Solicitud de canciones por álbum
#### 📤 **Método:** `GET`
#### 🔗 **Endpoint:** `https://api.spotify.com/v1/albums/{album_id}/tracks`

#### 📄 **Parámetros opcionales:**
- `limit`: número de canciones por solicitud
- `offset`: paginación

#### 📥 Respuesta esperada (JSON - Ejemplo):

```json
{
  "items": [
    {
      "id": "track123",
      "name": "Canción 1",
      "duration_ms": 210000,
      "track_number": 1
    }
    ...
  ]
}
```

📂 **Para ver una respuesta completa, consulta el archivo:** [`example_get_album_tracks.json`](./example_get_album_tracks.json)



## 📀 4. Obtención de detalles de un álbum
🔗 [Documentación Oficial](https://developer.spotify.com/documentation/web-api/reference/get-an-album)

Este servicio permite obtener información detallada de un álbum específico.

### Solicitud de detalles del álbum
#### 📤 **Método:** `GET`
#### 🔗 **Endpoint:** `https://api.spotify.com/v1/albums/{album_id}`

#### 📄 **Parámetros opcionales:**
- `market`: código de país para filtrar disponibilidad (Ejemplo: US)

#### 📥 Respuesta esperada (JSON - Ejemplo):

```json
{
  "id": "12345",
  "name": "Álbum Ejemplo",
  "release_date": "2025-03-26",
  "total_tracks": 10,
  "artists": [
    ....
  ]
  ...
}
```

📂 **Para ver una respuesta completa, consulta el archivo:** [`example_get_album.json`](./example_get_album.json)



## 🎤 5. Obtención de información de múltiples artistas
🔗 [Documentación Oficial](https://developer.spotify.com/documentation/web-api/reference/get-multiple-artists)

Este servicio permite obtener información de varios artistas a la vez mediante sus IDs.

### Solicitud de información de múltiples artistas
#### 📤 **Método:** `GET`
#### 🔗 **Endpoint:** `https://api.spotify.com/v1/artists`

#### 📄 **Parámetros opcionales:**
- `ids`: lista de IDs de artistas separada por comas (máximo 50 por solicitud)

#### 📥 Respuesta esperada (JSON - Ejemplo):

```json
{
  "artists": [
    {
      "id": "artist123",
      "name": "Artista X",
      "genres": ["pop", "rock"],
      ....
    }
  ]
}
```

📂 **Para ver una respuesta completa, consulta el archivo:** [`example_get_artists.json`](./example_get_artists.json)



## 🎧 6. Obtención de información de múltiples canciones
🔗 [Documentación Oficial](https://developer.spotify.com/documentation/web-api/reference/get-several-tracks)

Este servicio permite obtener información detallada de varias canciones a la vez, utilizando una lista de IDs. Es útil para recuperar atributos como la duración, el número de pista, la disponibilidad por país y especialmente la popularidad de cada canción.

### Solicitud de información de múltiples canciones
#### 📤 **Método:** `GET`
#### 🔗 **Endpoint:** `https://api.spotify.com/v1/artists`

#### 📄 **Parámetros opcionales:**
- `ids`:  lista de IDs de canciones separadas por comas (máximo 50 por solicitud)

#### 📥 Respuesta esperada (JSON - Ejemplo):

```json
{
  "tracks": [
    {
      "id": "track123",
      "name": "Canción 1",
      "popularity": 64,
      "duration_ms": 210000,
      "explicit": true,
      "available_markets": ["AR", "US", "MX"],
      ...
    },
    ...
  ]
}

```

📂 **Para ver una respuesta completa, consulta el archivo:** [`example_get_tracks.json`](./example_get_tracks.json)












## 🔄 Flujo de obtención de datos

1️⃣ Obtener el **token de acceso** desde el servicio de autenticación.

2️⃣ Consultar **nuevos lanzamientos** con el token obtenido.

3️⃣ Obtener los detalles de cada **álbum** usando su ID.

4️⃣ Obtener las **canciones** de cada álbum.

5️⃣ Obtener la **popularidad de las canciones** utilizando el endpoint de múltiples canciones. *Este paso es esencial ya que la popularidad no está disponible cuando se obtienen las canciones de un álbum.* 

6️⃣ Obtener información de los **artistas** relacionados.

7️⃣ Cargar los datos en **BigQuery** para luego transformarlos con **DBT** y facilitar su análisis y visualización.








📌 **Nota:** Todas las solicitudes deben incluir el token en los encabezados:

```bash
-H "Authorization: Bearer ACCESS_TOKEN"
```

## ⚠️ Política de Almacenamiento
Dado que los términos de uso de la API de Spotify prohíben el almacenamiento permanente de datos, este proyecto sigue las siguientes prácticas:

- **Almacenamiento temporal:** los datos se almacenan solo por un período breve (unas semanas) y luego se eliminan automáticamente.

- **Eliminación automática:** se han implementado mecanismos para limpiar los datos periódicamente, ya sea mediante reglas de expiración en Google Cloud Storage (GCS) o scripts de eliminación en BigQuery.

- **Uso restringido:** los datos solo se utilizan dentro del contexto académico del proyecto, sin distribución ni monetización.

- **Cumplimiento de políticas:** se respeta la política de uso de la API de Spotify para garantizar el cumplimiento de sus condiciones.

Si trabajas con este repositorio, asegúrate de seguir estas mismas prácticas y no almacenar datos de Spotify de manera indefinida.