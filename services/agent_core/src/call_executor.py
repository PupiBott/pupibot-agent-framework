import json
import uuid

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuración de sesión robusta: 3 reintentos en fallos 5xx, con backoff
session = requests.Session()
retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries))


def call_agent_runner_api(base_url: str, function_name: str, args: dict):
    """Ejecuta llamadas HTTP a agent-runner con manejo de retries y un Request ID."""

    # Generar Request ID para trazabilidad
    request_id = str(uuid.uuid4())
    headers = {"Content-Type": "application/json", "X-Request-Id": request_id}

    # Límite de tiempo total para evitar bloqueos
    TOTAL_TIMEOUT = 10

    if function_name == "createOperationOperationsPost":
        # Ejecución POST /operations
        r = session.post(
            f"{base_url}/operations", json=args, headers=headers, timeout=TOTAL_TIMEOUT
        )
    elif function_name == "executeActionV1AgentExecutePost":
        # Ejecución POST /v1/agent/execute
        r = session.post(
            f"{base_url}/v1/agent/execute",
            json=args,
            headers=headers,
            timeout=TOTAL_TIMEOUT,
        )
    else:
        # Esto nunca debería pasar si Gemini usa el Tool correcto
        return {
            "error": f"Función no implementada o fuera del contrato: {function_name}",
            "request_id": request_id,
        }

    # Lanza excepción HTTP si hay un error 4xx/5xx (que Retry no resolvió)
    r.raise_for_status()
    return r.json()
