# 🏗 Modelado de Datos con DBT

Este proyecto implementa el proceso de modelado de datos utilizando DBT (Data Build Tool), centrado en la creación de modelos para datos musicales extraídos de la API de Spotify. El objetivo es transformar datos crudos en información analítica valiosa, organizada en un modelo de datos estructurado que facilita el análisis de aspectos clave como la popularidad, géneros musicales, artistas, álbumes y más.

El modelo sigue las mejores prácticas de DBT y está organizado en tres categorías principales: modelos de staging, dimensiones y tablas de hechos. Esta estructura permite una fácil expansión y un análisis eficiente de los datos. Además, se incorpora la validación de la calidad de los datos mediante tests automatizados, documentación detallada y una estricta adherencia a buenas prácticas de desarrollo.



## Entorno de desarrollo

Crear entorno e instalar dependencias con pipenv

```bash
pipenv --python 3.12
```

```bash
pipenv install dbt-core dbt-bigquery 
```


## Configuración inicial

Para configurar el entorno y asegurar la correcta conexión con BigQuery, sigue los pasos detallados a continuación.


### Paso 1: Configurar la cuenta de servicio en GCP
Se requiere una cuenta de servicio con los siguientes permisos en BigQuery:
- `BigQuery Data Editor`
- `BigQuery Job User`
- `BigQuery User`

Para más detalles sobre la creación de cuentas y asignación de permisos, consulta el archivo [`setup_gcp_project.md`](../docs/setup_gcp_project.md).

Luego de configurar la cuenta descarga el archivo de credenciales y guárdalo en un lugar seguro.

**⚠️ Importante: no subas este archivo a GitHub.**


### Paso 2: Instalar DBT y dependencias
Instalar DBT localmente junto con la dependencia necesaria para conectar con BigQuery. En la sección de `Entorno de desarrollo`, encontrarás el listado completo de dependencias a instalar.


### Paso 3: Inicializar un proyecto DBT
Ejecuta los siguientes comandos para iniciar un nuevo proyecto en DBT:

```bash
pipenv shell
dbt init musics_data_modeling
```


### Paso 4: Configurar `profiles.yml`
Durante la inicialización, DBT te pedirá algunos datos de configuración. Entre ellos:

- Base de datos: ¿qué base de datos deseas usar?
- Método de autenticación: opción de autenticación deseada.
- Archivo de clave: ruta del archivo de credenciales de BigQuery.
- Proyecto: ID del proyecto en GCP.
- Dataset: nombre del dataset en BigQuery.
- Número de hilos: 1 o más.
- Tiempo máximo de ejecución de jobs.
- Ubicación: región donde está el dataset.


### Paso 5: Verificar la estructura del proyecto
Abre el archivo `dbt_project.yml` dentro de la carpeta `musics_data_modeling` para asegurarte de que la configuración del proyecto es correcta.


### Paso 6: Validar la conectividad con BigQuery
Para confirmar que la conexión con BigQuery es correcta, ejecuta el siguiente comando dentro del directorio del proyecto:

```bash
cd musics_data_modeling
dbt debug
```


### Paso 7: Ejecutar el proyecto DBT
Una vez que hayas creado tus modelos y configurado correctamente las conexiones, puedes ejecutar los modelos con el siguiente comando:

```bash
dbt run
```
Este comando compila y ejecuta todos los modelos definidos en tu proyecto sobre BigQuery.


### Paso 8: Ejecutar los tests
Para validar la calidad de tus datos, puedes ejecutar los tests definidos en tus archivos `.yml`:

```bash
dbt test
```
Esto incluye tanto los tests genéricos (`not_null`, `unique`, etc.) como los tests personalizados que hayas creado.


### Paso 9: Generar y visualizar la documentación
DBT permite generar una documentación navegable de todos tus modelos, tests y descripciones. Para hacerlo, sigue estos pasos:

#### **Generar la documentación**
Ejecuta el siguiente comando:

```bash
dbt docs generate
```
Esto crea un sitio web estático con toda la documentación definida en tus archivos `.yml`, incluyendo modelos, columnas, tests y descripciones.

#### **Visualizar la documentación**
Una vez generada, puedes abrirla en tu navegador ejecutando:

```bash
dbt docs serve
```
Esto levantará un servidor local (por defecto en `http://localhost:8080`) donde podrás navegar por tu proyecto, visualizar las relaciones entre modelos y explorar la metadata.



## Esquema del Modelo de Datos
A continuación, se describe la arquitectura general del modelo, incluyendo modelos de staging, dimensiones y tabla de hechos. Este esquema puede servir como documentación inicial o plantilla para ampliación futura.


### Modelos de Staging
Los modelos de staging tienen como objetivo **estandarizar**, **limpiar** y **transformar** la información cruda proveniente de la fuente original (Spotify API en este caso), dejándola lista para construir modelos de negocio como dimensiones y hechos. A continuación se detalla el propósito de cada uno.

#### **Staging Canciones (`stg_songs`)**
.**¿Qué representa?** - Este modelo representa el detalle de cada canción disponible en la plataforma, estandarizando y limpiando la información original proveniente de la API de Spotify. Incluye campos clave como nombre de la canción, duración, si es explícita o local, popularidad y su ubicación dentro del álbum (track y disc number).

**¿Para qué sirve?** - Permite analizar las canciones de forma individual, incluyendo su duración tanto en milisegundos como en segundos y minutos, si son populares o no, y si contienen contenido explícito. También asocia cada canción a su respectivo álbum y mercados disponibles para facilitar análisis posteriores, como popularidad por país, tendencias por tipo de canción, o categorización por duración.

#### **Staging Álbumes (`stg_albums`)**
**¿Qué representa?** - Este modelo describe los álbumes musicales disponibles en la plataforma. A partir de los datos brutos, estandariza los nombres, tipos, fechas de lanzamiento y otra información relevante del álbum, permitiendo una mejor organización y análisis de lanzamientos musicales.

**¿Para qué sirve?** - Permite realizar análisis como:
- Comparar popularidad entre diferentes tipos de álbumes (como sencillos vs. álbumes completos).
- Estudiar lanzamientos por año, mes o día según la precisión de la fecha.
- Investigar cuántas canciones contiene cada álbum y cuál es su sello discográfico.
- Evaluar la cantidad de lanzamientos a lo largo del tiempo o por sello.

#### **Staging Artistas (`stg_artists`)**
**¿Qué representa?** - Este modelo organiza la información de los artistas que participan en cada canción. A partir de los datos crudos, limpia y estandariza datos como el nombre del artista, su popularidad y su base de seguidores.

**¿Para qué sirve?** - Permite responder preguntas clave como:
- ¿Qué tan popular es un artista dentro de la plataforma?
- ¿Cuántos seguidores tiene un artista en el momento en que se insertó el dato?
- ¿Qué canciones están asociadas a cada artista?

Esto ayuda a realizar análisis de colaboraciones entre artistas, identificar a los más populares, y observar la evolución del impacto de un artista en relación con sus canciones.

#### **Staging Mercados Disponibles (`stg_available_markets`)**
**¿Qué representa?** - Este modelo muestra los países donde cada canción está disponible en Spotify, enriquecido con el nombre del país correspondiente. Utiliza los códigos ISO de dos letras (por ejemplo, US, AR) y los cruza con una tabla de referencia para mostrar también el nombre del país.

Los datos de países se enriquecen usando una semilla (`seed`) llamada `countries_iso`, que contiene los códigos y nombres de países reconocidos a nivel internacional.

**¿Para qué sirve?** - Permite analizar:
- La cobertura internacional de cada canción.
- Cuántos y cuáles países pueden acceder a cierto contenido musical.
- Tendencias de disponibilidad geográfica para decisiones de marketing, distribución o licencias

Esta información es útil para estudios de expansión de artistas, evaluación de cobertura internacional, y personalización de contenido por región.

#### **Staging Géneros Musicales por Artista (`stg_artists_genres`)**
**¿Qué representa?** - Este modelo muestra los géneros musicales asociados a cada artista. A partir de los datos brutos, se organiza la información para que podamos conocer el estilo o los estilos musicales de cada artista de forma clara.

Toma los géneros desde una estructura anidada y los relaciona con el identificador del artista. Solo se consideran los géneros válidos (es decir, no nulos).

**¿Para qué sirve?** - Permite:
- Analizar qué géneros predominan entre los artistas.
- Agrupar canciones o álbumes por estilo musical.
- Realizar recomendaciones musicales o análisis de tendencias por género.

#### **Staging Imágenes de Artistas (`stg_artists_images`)**
**¿Qué representa?** - Este modelo contiene las imágenes públicas de los artistas disponibles en la plataforma (por ejemplo, fotos de perfil o imágenes promocionales).

Extrae las imágenes de una estructura anidada y las relaciona con su artista correspondiente, incluyendo información como la URL, el alto y el ancho de cada imagen. Solo se incluyen imágenes válidas (que tienen una URL).

**¿Para qué sirve?** - Permite:
- Mostrar visualmente a los artistas en dashboards o apps.
- Analizar las proporciones o resoluciones más comunes en las imágenes.
- Enriquecer perfiles de artista con contenido visual.

### Tablas de Dimensiones
Las dimensiones representan entidades clave del negocio, como álbumes, artistas o canciones. Se construyen a partir de los modelos de staging y contienen información depurada, transformada y enriquecida para su uso en análisis, reportes o dashboards. Estas tablas permiten responder preguntas del tipo: *¿qué tan popular es un artista?, ¿cuáles son los álbumes recientes con más canciones explícitas?, o ¿en qué países está disponible una canción?*

#### **Dimensión de Álbumes (`dim_albums`)**
**¿Qué representa?** - Esta dimensión describe cada álbum musical presente en la plataforma. Se trata de una tabla central para entender las características generales de los álbumes disponibles, enriquecida con métricas derivadas de las canciones que lo componen.

**¿Para qué sirve?** - Permite:
- Identificar álbumes populares según su puntaje de popularidad.
- Clasificarlos según recencia (nuevo, reciente, clásico).
- Analizar duraciones máximas, mínimas y promedio de canciones por álbum.
- Explorar el número de canciones explícitas y la cantidad total de pistas.
- Evaluar la longitud del álbum y su popularidad en conjunto.

#### **Dimensión de Artistas (`dim_artists`)**
**¿Qué representa?** - Contiene información agregada sobre cada artista, incluyendo su popularidad, seguidores, géneros musicales y cantidad de imágenes disponibles.

**¿Para qué sirve?** - Permite:
- Entender el nivel de influencia del artista a través de seguidores y popularidad.
- Analizar la diversidad de géneros que abarca un artista.
- Medir la cantidad de contenido visual (imágenes).
- Comparar artistas según distintas métricas (promedio, máximo y mínimo de popularidad y seguidores).


#### **Dimensión de Canciones (`dim_songs`)**
**¿Qué representa?** - Describe cada canción individual, incluyendo su duración, tipo, popularidad, artistas asociados, su álbum, y en qué países está disponible.

**¿Para qué sirve?** - Permite:
- Clasificar canciones por duración (corta, media, larga) o por popularidad.
- Identificar si una canción es explícita o local.
- Ver cuántos artistas participan y sus nombres.
- Analizar la disponibilidad internacional de la canción (países).
- Relacionar la canción con atributos del álbum como su recencia y popularidad.


### Tablas de Hechos
Las tablas de hechos permiten analizar relaciones entre entidades, realizar cálculos agregados y responder preguntas cuantitativas. Se construyen a partir de la combinación de dimensiones y staging models, y se utilizan para crear métricas, indicadores clave (KPIs) y visualizaciones en dashboards.

#### **Contribuciones de Artistas por Álbum (`fact_artist_album_contributions`)**

**¿Qué representa?** - Esta tabla de hechos detalla la contribución de cada artista a los álbumes en los que participa, midiendo la cantidad de canciones en las que colabora dentro de un álbum específico. Combina información de los modelos de staging y dimensiones para entender mejor la relación entre artistas y álbumes.

**¿Para qué sirve?** - Permite:
- Saber cuántas canciones de un álbum fueron interpretadas por un determinado artista.
- Calcular el porcentaje de participación de un artista dentro de un álbum.
- Identificar si un artista es el único que participa en todo el álbum.
- Cruzar características de los álbumes (como popularidad o duración) con los perfiles de los artistas (géneros, seguidores, popularidad máxima).
- Crear visualizaciones sobre colaboraciones y participación individual o grupal dentro de álbumes musicales.

#### **Métricas de Artistas por Álbum (`fact_album_artist_metrics`)**

**¿Qué representa?** - Esta tabla de hechos sintetiza métricas clave por combinación de artista y álbum, mostrando cómo se comportan los artistas dentro de cada álbum en el que participan. Integra información proveniente de los modelos de dimensión de artistas, álbumes y canciones, agrupada por artista y álbum.

**¿Para qué sirve?** - Permite:
- Analizar el desempeño de un artista dentro de un álbum específico (popularidad, duración media de canciones, contenido explícito).
- Comparar álbumes según la participación de artistas y la naturaleza de sus canciones.
- Clasificar y categorizar la duración y popularidad promedio de canciones por artista en un álbum.
- Usar las características del artista (géneros, cantidad de imágenes, popularidad media) y del álbum (tipo, año, popularidad) para análisis detallados.
- Facilitar visualizaciones y dashboards que combinen dimensiones artísticas y editoriales (álbumes) para entender tendencias de producción y colaboración musical.


## Buenas Prácticas
- Usa macros para reutilizar lógica, por ejemplo: formateo de tiempo, categorización de duración o popularidad.
- Define tests genéricos para asegurar la integridad del modelo.
- Mantén la documentación de cada campo actualizada usando archivos `.yml`.
- Organiza los modelos en carpetas: `staging`, `core`, `intermediate`, `marts`, etc.
