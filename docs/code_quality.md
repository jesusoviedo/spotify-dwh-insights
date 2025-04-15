# Configuración y Herramientas de Calidad de Código
Este archivo describe cómo configurar y utilizar las herramientas de calidad de código en este proyecto, específicamente `pre-commit`, `black`, `ruff` e `isort`. Estas herramientas se utilizan para mantener un código limpio y estandarizado.
 
## Herramientas
### pre-commit
El proyecto usa pre-commit para ejecutar automáticamente herramientas de formateo y linters antes de realizar un commit. Esto asegura que el código sigue los estándares de estilo y está libre de errores comunes.

¿Qué es el archivo `.pre-commit-config.yaml`?
El archivo `.pre-commit-config.yaml` contiene la configuración para los hooks de pre-commit. Cada hook ejecuta una herramienta diferente que valida y formatea el código.

**Hooks incluidos:**
- **black**: Formatea el código automáticamente según el estilo de PEP 8.
- **ruff**: Linter para detectar errores y mejorar la calidad del código.
- **isort**: Organiza las importaciones en orden conforme a las convenciones de Python.

## Configuración
### 1. Instalación de pre-commit
Para instalar `pre-commit`, ejecuta el siguiente comando:
```bash
pip install pre-commit
```

### 2. Instalar los hooks
Una vez que `pre-commit` esté instalado, puedes instalar los hooks definidos en el archivo `.pre-commit-config.yaml` con el siguiente comando:
```bash
pre-commit install
```

### 3. Ejecutar hooks manualmente
Si deseas ejecutar los hooks manualmente sobre todos los archivos del proyecto, puedes hacerlo con:
```bash
pre-commit run --all-files
```

De esta forma, puedes asegurarte de que el código cumple con los estándares de calidad antes de hacer un commit.
