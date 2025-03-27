# Gestión de entorno virtuales con Pipenv

Para trabajar con Python de manera local, se recomienda utilizar Pipenv, una herramienta que combina la gestión de entornos virtuales y la instalación de dependencias en un solo flujo de trabajo.

Con Pipenv, puedes:
- Crear un entorno virtual aislado para tu proyecto.
- Instalar y gestionar dependencias de forma sencilla con un Pipfile.
- Bloquear versiones exactas de las dependencias en Pipfile.lock para garantizar reproducibilidad.

## Ejemplo de uso
1. Instalar Pipenv (si no lo tienes):
```bash
pip install pipenv
```


2. Crear un entorno virtual e instalar dependencias:
```bash
pipenv --python 3.12 #u otra version instalada de python
pipenv install requests
```


3. Activar el entorno virtual:
```bash
pipenv shell
```


4. Ejecutar scripts dentro del entorno:
```bash
python script.py
```


Esto garantiza que el proyecto tenga un entorno limpio y controlado sin afectar el sistema global de Python.

## Documentación

Para obtener más información sobre el uso de Pipenv, puedes consultar su documentación oficial en:

🔗 [Pipenv Documentation](https://pipenv.pypa.io/en/latest/)