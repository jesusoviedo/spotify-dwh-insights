# Scripts

Esta carpeta contiene scripts en Python para interactuar con la API de Spotify, así como para crear recursos en **Google Cloud Storage (GCS)** y **Compute Engine**.

Antes de consumir la API de Spotify, es necesario completar algunos pasos previos, los cuales se explican en el archivo [`README.md`](../data/README.md) de la carpeta `data`. Allí encontrarás una guía rápida sobre cómo autenticarte y utilizar el servicio de Spotify, junto con ejemplos de respuestas de los endpoints que se emplearán en este proyecto.

## Entorno de desarrollo

Crear entorno e instalar dependencias con pipenv

```bash
pipenv --python 3.12
```

```bash
pipenv install requests pandas pyarrow
```

## Configuración necesaria para `api_spotify.py`
Antes de ejecutar el script `api_spotify.py`, es necesario establecer las siguientes variables de entorno:
- `CLIENTE_ID`: el ID de cliente para autenticarte en la API de Spotify.
- `CLIENTE_SECRET`: el secreto de cliente para autenticarte en la API de Spotify.

1. Establecer las Variables de Entorno en Linux (Terminal Bash)
En la terminal, antes de ejecutar el script, puedes setear las variables de entorno con los siguientes comandos:

```bash
export CLIENTE_ID="tu_cliente_id"
export CLIENTE_SECRET="tu_cliente_secret"
```

Sustituye "tu_cliente_id" y "tu_cliente_secret" por tus valores reales.

2. Verificar que las Variables se Establecieron Correctamente
Para asegurarte de que las variables de entorno se configuraron correctamente, puedes ejecutar los siguientes comandos:

```bash
echo $CLIENTE_ID
echo $CLIENTE_SECRET
```

Si todo está bien configurado, deberías ver los valores de tus variables. Con esto, ya podrás ejecutar el script `api_spotify.py` correctamente."
