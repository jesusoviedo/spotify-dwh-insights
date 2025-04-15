# Configuración y Herramientas de Calidad de Código

Este archivo describe cómo configurar y utilizar las herramientas de calidad de código en este proyecto, específicamente `pre-commit` y una serie de herramientas como `black`, `ruff`, `isort`, `mypy`, entre otras. Estas herramientas se utilizan para mantener un código limpio, estandarizado y libre de errores comunes.

## Herramientas
### pre-commit
El proyecto usa `pre-commit` para ejecutar automáticamente herramientas de formateo, análisis estático y validación antes de realizar un commit. Esto asegura que el código sigue los estándares de estilo y no incluye errores comunes, archivos sensibles o código muerto.

### ¿Qué es el archivo `.pre-commit-config.yaml`?

El archivo `.pre-commit-config.yaml` contiene la configuración para los hooks de pre-commit. Cada hook ejecuta una herramienta diferente que valida, formatea o inspecciona el código antes de hacer commit.

### **Hooks incluidos:**

#### **Validaciones de seguridad y formato general**
- **check-added-large-files**: Detecta archivos grandes añadidos accidentalmente al repo.
- **check-case-conflict**: Detecta conflictos de nombres de archivos que podrían fallar en sistemas case-insensitive.
- **check-json** y **check-yaml**: Validan archivos `.json` y `.yaml` respectivamente.
- **detect-private-key**: Detecta si se intenta commitear una clave privada por accidente.
- **end-of-file-fixer**: Asegura que todos los archivos terminen con una línea nueva.
- **gitleaks**: Detecta secretos y credenciales comprometidas.

#### **Herramientas específicas para Python**
- **black**: Formatea el código automáticamente según el estilo PEP 8 (con línea máxima de 120 caracteres).
- **ruff**: Linter rápido y configurable para código Python.
- **isort**: Organiza las importaciones de forma coherente (usando perfil de `black`).
- **mypy**: Realiza verificación de tipos en el código Python.
- **dead**: Detecta código Python muerto o sin uso.
- **rm-unneeded-f-str**: Elimina `f-strings` innecesarios en cadenas simples.



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
