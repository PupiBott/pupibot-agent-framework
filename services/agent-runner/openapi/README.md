# OpenAPI Snapshot y Artefactos

## Cómo regenerar el snapshot localmente

1. Asegúrate de tener todas las dependencias instaladas:
   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta el siguiente comando desde la raíz del proyecto:
   ```bash
   python -c "from services.agent_runner.src.main import app; import json; open('openapi.snapshot.json', 'w').write(json.dumps(app.openapi(), indent=2))"
   ```

3. El archivo `openapi.snapshot.json` será actualizado en la raíz del proyecto.

## Ruta del snapshot
El snapshot actual se encuentra en la raíz del repositorio con el nombre `openapi.snapshot.json`.

## Política de artefactos
- Los artefactos generados en CI (`openapi.current.json`) se suben automáticamente con el ID del run para trazabilidad.
- Revisión manual: Los artefactos deben revisarse y eliminarse si no son necesarios.
- Limpieza periódica: Implementar un script o job cron para limpiar artefactos antiguos si el almacenamiento se vuelve un problema.