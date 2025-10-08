# Proyecto de Asistente IA Local

Este proyecto es una base para desarrollar un asistente de inteligencia artificial local. Incluye configuraciones iniciales y una estructura de carpetas organizada para facilitar el desarrollo.

## Instalación de dependencias de desarrollo

Primero, activa el entorno virtual existente:

```bash
source .venv/bin/activate
```

Luego, instala las dependencias de desarrollo:

```bash
pip install -r requirements-dev.txt
```

**Nota:** Asegúrate de usar siempre el entorno virtual `.venv` para evitar conflictos con dependencias globales.

## Inicialización de la base de datos

En producción, la función `initialize_database()` se llama sin argumentos y crea el archivo `operations.db` en disco.

En los tests, se pasa una conexión SQLite en memoria a `initialize_database()` para evitar bloqueos y errores de concurrencia.

# Database Behavior

## Production
In production, the `initialize_database` function creates a connection to the SQLite database on disk (`operations.db`) and ensures the `operations` table exists. The connection is created and closed within the function to ensure proper resource management.

## Testing
During testing, an in-memory SQLite database is used. The `initialize_database` function is passed an open connection, which remains open for the entire test suite. This ensures test isolation and avoids interference with the production database. The connection is managed by pytest and is automatically closed at the end of the test suite.