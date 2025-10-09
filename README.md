# 🤖 PUPIBOT: Agente Modular de Orquestación y Creación de Contenido (GenAI)

## 🌟 Visión General

PUPIBOT es un **Framework de Orquestación de Agentes de IA** diseñado para transformar instrucciones en acciones complejas que involucran múltiples servicios. Va más allá de una simple conversación: actúa como un **cerebro central** capaz de controlar microservicios y APIs externas, permitiendo la creación automatizada de activos de alto valor como presentaciones interactivas, documentos y contenido multimedia.

Este proyecto es una **prueba de concepto (PoC)** de arquitectura modular y *serverless* para la nueva era de aplicaciones basadas en *Large Language Models (LLMs)*.

## ⚙️ Arquitectura Técnica

El proyecto sigue una arquitectura de **Microservicios orquestados en Docker Compose**, lo que garantiza portabilidad y estabilidad.

| Componente | Rol | Tecnología Clave |
| :--- | :--- | :--- |
| **`agent-runner` (El Cerebro)** | Núcleo de la aplicación. Recibe peticiones, decide qué servicio llamar (la **orquestación**) y maneja las llamadas a las APIs externas. | FastAPI, Python, **`httpx`** (para llamadas asíncronas) |
| **`document-service` (Ejemplo)**| Servicio de ejemplo que simula la generación de documentos (PDFs, Docs). Es un *placeholder* para módulos futuros (YouTube, Correo, Presentaciones). | FastAPI, Docker |
| **`docker-compose`** | Define el entorno completo, permitiendo que el proyecto se levante con un solo comando. | Docker |

## 🧪 Pruebas y Calidad del Código

La estabilidad se garantiza mediante una sólida suite de pruebas.

* **Pruebas de Integración:** Se utiliza `pytest-httpx` para simular (mockear) las respuestas de los microservicios, verificando que el `agent-runner` interactúe correctamente con los servicios externos sin depender de la red real.
* **Soporte Asíncrono:** La suite utiliza `pytest-asyncio` para probar la lógica asíncrona de manera segura y determinista.

---

## 🛠️ Instalación y Uso (Local)

1.  **Clonar el repositorio:** `git clone https://github.com/PupiBott/pupibot-agent-framework.git`
2.  **Entrar a la carpeta:** `cd pupibot-agent-framework`
3.  **Levantar el entorno:** `docker compose up --build`
4.  **Acceder al Cerebro (Agent Runner):** `http://localhost:8000/docs` (Documentación OpenAPI)

---

## 🛣️ Próximos Pasos (Roadmap)

1. **Interfaz de Usuario (UI):** Conexión de una interfaz *frontend* para la interacción humana.
2. **Nuevos Módulos:** Implementar los servicios de creación de **Podcast Interactivo** y **Presentaciones Dinámicas** para *onboarding* corporativo.
3. **Persistencia:** Conexión a una base de datos para almacenar el historial de operaciones (`op_id`).
# Trigger update
