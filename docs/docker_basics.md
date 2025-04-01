# Docker y Docker Compose

## Verificar la instalación
Para comprobar si tienes Docker instalado ejecuta:
```bash
docker --version 
```

Para verificar Docker Compose:
```bash
docker compose version
```

Si no están instalados, puedes seguir las instrucciones oficiales:
- 🔗 [Docker Docs](https://docs.docker.com/get-started/get-docker/)
- 🔗 [Docker Compose Docs](https://docs.docker.com/compose/install/)


## Docker

A continuación, se presentan algunos de los comandos más utilizados en Docker para gestionar contenedores, imágenes y redes.

### Gestión de Contenedores
**Listar contenedores en ejecución:** muestra todos los contenedores que están en ejecución actualmente.
```bash
docker ps
```


**Listar todos los contenedores (en ejecución y detenidos):** muestra todos los contenedores, incluidos los que no están en ejecución.
```bash
docker ps -a
```


**Iniciar un contenedor detenido:** inicia un contenedor previamente detenido.
```bash
docker start <container_id>
```


**Detener un contenedor en ejecución:** detiene un contenedor en ejecución.
```bash
docker stop <container_id>
```


**Eliminar un contenedor:** elimina un contenedor, ya sea en ejecución o detenido.
```bash
docker rm <container_id>
```


### Gestión de Imágenes
**Listar las imágenes locales:** muestra todas las imágenes disponibles localmente.
```bash
docker images
```


**Eliminar una imagen:** elimina una imagen que ya no se necesita.
```bash
docker rmi <image_id>
```


**Construir una imagen desde un Dockerfile**: crea una nueva imagen a partir de un archivo `Dockerfile`. 
```bash
docker build -t <image_name>:<tag> .
```

*El parámetro `-t` permite asignar un nombre y una etiqueta (tag) a la imagen. El `.` al final indica que el contexto de construcción es el directorio actual.*


**Descargar una imagen desde Docker Hub:** descarga una imagen desde el registro oficial de Docker (Docker Hub).
```bash
docker pull <image_name>
```


### Gestión de Redes
**Listar redes:** muestra todas las redes creadas por Docker.
```bash
docker network ls
```


**Crear una nueva red:** crea una nueva red para conectar contenedores entre sí.
```bash
docker network create <network_name>
```


### Otras operaciones útiles
**Ver los logs de un contenedor:** muestra los logs de un contenedor en ejecución.
```bash
docker logs <container_id>
```


**Ejecutar un comando dentro de un contenedor:** ejecuta un comando en un contenedor en ejecución.
```bash
docker exec -it <container_id> <command>
```


### Comando para limpiar recursos no utilizados

**Eliminar contenedores detenidos, imágenes no utilizadas y redes no referenciadas:** limpia los recursos que ya no se están utilizando para liberar espacio en disco.
```bash
docker system prune
```

### Gestionar imágenes de Docker en Docker Hub

#### **Crear una cuenta en Docker Hub (si no la tienes)**
Si aún no tienes una cuenta en Docker Hub, crea una [aquí](https://hub.docker.com/).


#### **Iniciar sesión en Docker Hub desde la terminal**
Usa el siguiente comando para iniciar sesión en tu cuenta de Docker Hub:
```bash
docker login
```
Te pedirá tu nombre de usuario y contraseña. Si todo es correcto, verás un mensaje de éxito.


#### **Etiqueta la imagen**
Antes de subirla, necesitas etiquetar tu imagen para asociarla con tu repositorio de Docker Hub. La etiqueta debe seguir el formato:
`<username>/<repository>:<tag>`

Por ejemplo, si tu nombre de usuario en Docker Hub es `usuarioxyz` y el nombre del repositorio es `repositorio-123`:
```bash
docker tag <image_name>:<tag> usuarioxyz/repositorio-123:<tag>
```


#### **Subir la imagen a Docker Hub**
Ahora, sube la imagen etiquetada a Docker Hub con el siguiente comando:
```bash
docker push usuarioxyz/repositorio-123:<tag>
```


#### Descargar (pull) la imagen en otra máquina
Para verificar que la imagen se subió correctamente o usarla en otro lugar, puedes descargarla con el siguiente comando:
```bash
docker pull usuarioxyz/repositorio-123:<tag>
```


## Docker Compose

A continuación, se presentan algunos de los comandos más utilizados en Docker Compose.

### Construir contenedores
El siguiente comando construye los contenedores definidos en el archivo docker-compose.yml, descargando las imágenes necesarias y configurando los servicios:
```bash
docker compose build
```



### Iniciar los servicios
Este comando inicia los contenedores y los servicios definidos en el archivo docker-compose.yml. Si los contenedores aún no están construidos, el comando los construirá antes de iniciarlos:
```bash
docker compose up
```



### Iniciar en segundo plano
Al agregar la opción -d (detached), el comando inicia los servicios en segundo plano, permitiendo que puedas seguir utilizando la terminal para otras tareas:
```bash
docker compose up -d
```



### Detener los servicios
Este comando detiene y elimina los contenedores, redes y volúmenes creados por Docker Compose, devolviendo el entorno a su estado anterior:
```bash
docker compose down
```

## Documentación
Para obtener más información sobre el uso de Docker y Docker Compose, puedes consultar las documentaciones oficiales en:

- 🔗 [Docker Documentation](https://docs.docker.com/)
- 🔗 [Docker Compose Documentation](https://docs.docker.com/compose/)
