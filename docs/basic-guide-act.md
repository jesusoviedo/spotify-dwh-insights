# Guía de uso de act para ejecutar workflows de GitHub Actions en Linux

## ¿Qué es  `act`?
`act` es una herramienta de línea de comandos que permite ejecutar workflows de GitHub Actions de manera local, en tu máquina, sin necesidad de hacer push a GitHub. Esto es útil para probar y depurar tus workflows rápidamente.

## Instalación segura de act en Linux
A continuación, te explico cómo instalar `act` en tu máquina Linux de manera segura.

### 1. Descargar e instalar act
Ejecuta los siguientes comandos para descargar e [instalar](https://nektosact.com/installation/index.html) `act` en tu sistema:

```bash
# Descargar la última versión de act
curl -LO https://github.com/nektos/act/releases/latest/download/act_Linux_x86_64.tar.gz

# Extraer el archivo descargado
tar -xvzf act_Linux_x86_64.tar.gz

# Mover el binario a una carpeta dentro de tu $PATH
sudo mv act /usr/local/bin/

# Eliminar los archivos temporales
rm act_Linux_x86_64.tar.gz
```

### 2. Verificación de instalación
Para verificar que `act` se ha instalado correctamente, ejecuta el siguiente comando:

```bash
act --version
```

Si todo está bien, deberías ver la versión de `act` instalada en tu sistema.

## Configuración inicial de `act`
Antes de poder ejecutar tus workflows localmente, necesitas configurar algunos detalles en tu entorno.

### 1. Crear un archivo secrets (opcional)
Si tu workflow depende de secretos (como tokens o claves API), puedes configurarlos localmente en `act`. Crea un archivo llamado `.secrets` en el directorio donde tienes tu repositorio con el siguiente formato:

```bash
MY_SECRET=my-secret-value
ANOTHER_SECRET=another-secret-value
```

### 2. Configurar tu repositorio
Asegúrate de que tu repositorio tenga los archivos de workflow de GitHub Actions ubicados en la carpeta `.github/workflows/`. Si ya tienes configurados tus workflows en GitHub, solo necesitas clonarlos a tu máquina local.


### 3. Ejecutar workflows con `act`
Este comando ejecutará el workflow principal del repositorio.

```bash
act
```

Este comando ejecutará los workflows que están configurados para dispararse con el evento `push`.

```bash
act push
```

También puedes especificar un flujo de trabajo específico con el parámetro -W:

```bash
act -W .github/workflows/ci-qa-pre-commit.yml
```

Ahora que tienes act instalado y configurado, puedes ejecutar y depurar tus workflows de GitHub Actions localmente de manera eficiente, sin necesidad de hacer push a GitHub.
