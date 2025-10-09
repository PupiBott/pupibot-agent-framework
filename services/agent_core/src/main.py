import json
import os
from pathlib import Path

from google import genai
from google.genai import types

from .call_executor import call_agent_runner_api
from .tool_adapter import load_openapi_tool

AGENT_RUNNER_BASE_URL = os.environ.get("AGENT_RUNNER_URL", "http://127.0.0.1:8000")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")


def init_client():
    if not GEMINI_API_KEY:
        return None
    return genai.Client(api_key=GEMINI_API_KEY)


def run_agent_loop(prompt: str):
    """El bucle principal de Tool Calling que orquesta Gemini y la API."""
    client = init_client()
    if not client:
        print("ERROR: Clave de Gemini no disponible.")
        return

    OPENAPI_PATH = Path("services/agent-runner/openapi/openapi.json")
    tool = load_openapi_tool(str(OPENAPI_PATH))
    model = "gemini-2.5-flash"

    # Primer request a Gemini: ¿Qué acción debo tomar?
    response = client.models.generate_content(
        model=model, contents=[prompt], config=types.GenerateContentConfig(tools=[tool])
    )

    print(f"User Prompt: {prompt}\n")

    # Bucle de Tool Calling
    while response.function_calls:
        print("🤖 Gemini decidió llamar a una función...")

        tool_outputs = []
        for fc in response.function_calls:
            name = fc.name
            args = dict(fc.args)

            print(f"  > Función Solicitada: {name}")
            print(f"  > Argumentos: {args}")

            try:
                # Ejecutar la acción real a través del executor robusto
                result = call_agent_runner_api(AGENT_RUNNER_BASE_URL, name, args)
                tool_output_part = types.Part.from_function_response(
                    name=name, response={"result": json.dumps(result)}
                )
                tool_outputs.append(tool_output_part)
                print(f"  > Salida OK: {json.dumps(result)[:50]}...")
            except requests.exceptions.HTTPError as e:
                # Manejo de error HTTP (4xx/5xx)
                error_details = {
                    "error": f"HTTP Error: {e.response.status_code}",
                    "details": e.response.text[:100],
                }
                tool_output_part = types.Part.from_function_response(
                    name=name, response={"error": json.dumps(error_details)}
                )
                tool_outputs.append(tool_output_part)
                print(f"  > Error HTTP: {e.response.status_code}")
            except Exception as e:
                # Otros errores (conexión, timeout, etc.)
                error_details = {
                    "error": f"Error de Ejecución: {type(e).__name__}",
                    "details": str(e)[:100],
                }
                tool_output_part = types.Part.from_function_response(
                    name=name, response={"error": json.dumps(error_details)}
                )
                tool_outputs.append(tool_output_part)
                print(f"  > Error General: {type(e).__name__}")

        # Devolver resultados al modelo para el siguiente paso
        response = client.models.generate_content(
            model=model,
            contents=[prompt, response]
            + tool_outputs,  # Agregar el historial de la función y su output
            config=types.GenerateContentConfig(tools=[tool]),
        )

    # 5. Respuesta Final (Texto)
    print("\n✅ Respuesta Final del LLM:")
    print(
        getattr(response, "text", str(response))
    )  # Imprimir el resultado final del razonamiento


# CLI Entrypoint
if __name__ == "__main__":
    if not GEMINI_API_KEY:
        print("ERROR: La variable de entorno GEMINI_API_KEY debe estar configurada.")
        print('Ejecuta: export GEMINI_API_KEY="<TU_CLAVE>"')
        exit(1)

    # Ejemplo de uso forzado
    run_agent_loop(
        "Crea una nueva operación con la acción 'analyze_data' y el payload 'reporte_trimestral'."
    )
