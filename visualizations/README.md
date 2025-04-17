# 📈 Dashboard con Looker Studio

Este proyecto utiliza Looker Studio como herramienta de visualización para explorar y comunicar insights sobre la participación de artistas en álbumes musicales y métricas clave relacionadas con sus canciones.

El dashboard está compuesto por dos páginas interactivas, diseñadas para facilitar el análisis de tendencias, niveles de participación artística y características destacadas de las producciones musicales.

Los gráficos y visualizaciones están conectados a una fuente de datos que se actualiza automáticamente cada 12 horas, garantizando información siempre actualizada. Además, también se puede forzar una actualización manual bajo demanda, permitiendo incorporar rápidamente nuevos datos cuando sea necesario.

A continuación se detalla lo que podés encontrar en cada una de las páginas del dashboard:


## 🎨 Página 1 – Contribuciones de Artistas en Álbumes
🔗 [Ver en Looker Studio](https://lookerstudio.google.com/u/0/reporting/07fc8408-5e48-480d-90c9-24fc41dd6d41/page/VoZGF)

Esta página está construida a partir de la tabla de hechos `fact_artist_album_contributions` y ofrece una visión integral sobre cómo los artistas participan en la creación de álbumes musicales.

### 📊 ¿Qué vas a encontrar?
- **Indicadores claves que resumen:**
    - Total de álbumes analizados
    - Total de artistas participantes
    - Popularidad máxima y mínima entre artistas
    - Álbumes con más y menos canciones
    - Promedio de duración de canciones por álbum

- **Gráficos dinámicos para explorar tendencias y comparaciones:**
    - Barras que muestran la cantidad de álbumes por artista
    - Clasificación de popularidad de los álbumes
    - Gráfico de anillos con la distribución de álbumes populares
    - Línea de tiempo con fechas de lanzamiento de álbumes, donde también se visualiza:
        - El promedio de duración de canciones por fecha
        - La máxima cantidad de canciones en un álbum por fecha
- **Tabla detallada con:**
    - Artista, álbum, cantidad de canciones aportadas, duración promedio de las canciones del álbum (en minutos), total de canciones del álbum y porcentaje de participación del artista

### 🧠 ¿Qué insights se pueden obtener?
Esta página permite responder preguntas como:
- ¿Qué artistas tienen mayor presencia en álbumes recientes?
- ¿Cómo varía la popularidad entre álbumes y artistas?
- ¿Los álbumes más recientes tienden a ser más largos o más cortos?
- ¿Qué artistas lideran en términos de participación dentro de un álbum?
- ¿Cómo ha evolucionado la producción musical (duración, cantidad de temas) a lo largo del tiempo?

Además, los filtros interactivos permiten segmentar la información por artistas, álbumes específicos, rangos de fechas y duración promedio, lo que facilita un análisis más profundo y adaptado a diferentes enfoques.



## 🎶 Página 2 – Exploración de Canciones por Artista
🔗 [Ver en Looker Studio](https://lookerstudio.google.com/u/0/reporting/07fc8408-5e48-480d-90c9-24fc41dd6d41/page/p_csuznxbhrd)

Esta página está construida a partir de la tabla de hechos `fact_album_artist_metrics` y se enfoca en analizar el perfil musical de los artistas a través de las canciones que han interpretado o lanzado.

### 📊 ¿Qué vas a encontrar?
- **Indicadores claves que resumen:**
    - Total de artistas analizados
    - Total de canciones
    - Total de canciones explícitas
    - Promedio de géneros asociados a los artistas
    - Promedio de popularidad de las canciones
    - Promedio de duración de canciones (en minutos)

- **Gráficos para explorar tendencias musicales:**
    - Gráfico de barras con la cantidad de canciones lanzadas por año
    - Gráfico de barras que clasifica a los artistas según su categoría de popularidad
    - Gráfico de anillos que agrupa canciones por categoría de duración promedio

- **Gráfico de burbujas para visualizar artistas según:**
    - Eje X: Total de canciones
    - Eje Y: Duración promedio de canciones
    - Tamaño de la burbuja: Popularidad promedio del artista

- **Tabla comparativa con el ranking de artistas según:**
    - Popularidad promedio
    - Duración promedio de sus canciones

### 🧠 ¿Qué insights se pueden obtener?
Esta página permite responder preguntas como:
- ¿Qué artistas tienen mayor volumen de canciones lanzadas?
- ¿Qué tan populares son los artistas con más producciones?
- ¿Qué tendencias se observan en la duración promedio de canciones?
- ¿Qué artistas logran un equilibrio entre cantidad, duración y popularidad?
- ¿Hay relación entre la popularidad y la longitud promedio de sus canciones?

Además, podés utilizar los filtros interactivos para enfocar el análisis en artistas específicos, años de lanzamiento o rangos de duración y popularidad, ajustando la exploración según el objetivo de tu análisis.
