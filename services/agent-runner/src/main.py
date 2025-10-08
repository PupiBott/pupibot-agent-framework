from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import sqlite3
import logging
import uuid
import asyncio
import httpx
import json
import os
from fastapi import Request, HTTPException, status
from contextlib import asynccontextmanager
import traceback  # Add this at the top of the file
import sys
from pathlib import Path

# Garantiza que la carpeta services/agent-runner se inserte en sys.path
# para que las importaciones `from src.*` funcionen cuando se ejecute
# uvicorn desde la raíz del repo.
ROOT = Path(__file__).resolve().parents[2]  # -> /.../services/agent-runner
ROOT_STR = str(ROOT)
if ROOT_STR not in sys.path:
    sys.path.insert(0, ROOT_STR)

# Debugging sys.path
print("sys.path:", sys.path)

# Import database initialization
from src.db_init import initialize_database

# Determina si estamos en modo testing (controlado por env var)
IS_TESTING = os.environ.get("TESTING", "false").lower() in ("1", "true", "yes")

# Define lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = sqlite3.connect("operations.db", check_same_thread=False, timeout=30)
    app.state.db_conn = conn
    initialize_database(conn)
    yield
    if app.state.db_conn:
        app.state.db_conn.close()

# Initialize FastAPI app
app = FastAPI(
    title="PupiBot Agent Runner API",
    version="1.0.0",
    description="API para gestión y ejecución de operaciones por agentes",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger("agent-runner")

# Database setup
def set_db_connection(conn: sqlite3.Connection):
    app.state.db_conn = conn

def get_db_connection():
    if hasattr(app.state, "db_conn") and app.state.db_conn:
        try:
            app.state.db_conn.execute("SELECT 1")  # Check if connection is alive
            return app.state.db_conn
        except sqlite3.ProgrammingError:
            pass  # Connection is closed, recreate it

    conn = sqlite3.connect("operations.db", check_same_thread=False, timeout=30)
    conn.row_factory = sqlite3.Row  # Set row factory for dictionary-like access
    app.state.db_conn = conn

    logger.debug("Attempting to establish database connection")
    logger.debug("Database connection established successfully", extra={"db_conn": repr(conn)})

    return conn

# Middleware for Bearer Token Validation
@app.middleware("http")
async def validate_bearer_token(request: Request, call_next):
    # Rutas públicas que no deben requerir Authorization incluso en prod
    public_paths = {"/openapi.json", "/docs", "/redoc", "/health"}

    # Si estamos en modo testing, omitimos la validación por completo
    if IS_TESTING:
        return await call_next(request)

    # Permitir acceso público a docs/openapi/health siempre
    if request.url.path in public_paths or request.url.path.startswith("/docs/") or request.url.path.startswith("/redoc/"):
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

    token = auth_header.split(" ", 1)[1].strip()
    # Aquí va tu validación existente del token — no la cambies; reutilízala
    # ejemplo:
    # if not validate_token(token):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return await call_next(request)

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "agent-runner"}

# Pydantic models
class ExecuteRequest(BaseModel):
    action: str
    payload: dict
    idempotency_key: str

class OperationResponse(BaseModel):
    operation_id: int

class OperationStatus(BaseModel):
    operation_id: int
    status: str

class OperationIn(BaseModel):
    action: str
    payload: str
    idempotency_key: Optional[str] = None

class Operation(BaseModel):
    id: int = Field(..., description="ID único de la operación")
    action: str = Field(..., description="Tipo de acción que ejecuta la operación")
    payload: Optional[str] = Field(None, description="Datos asociados a la operación")
    status: Optional[str] = Field(None, description="Estado actual de la operación")
    result: Optional[dict] = Field(None, description="Resultado de la operación")

# Endpoints
@app.post("/v1/agent/execute", response_model=OperationResponse)
async def execute_action(request: ExecuteRequest):
    conn = get_db_connection()
    logger.debug(f"execute_action: acquired connection {repr(conn)}")
    cursor = conn.cursor()

    # Check for idempotency
    cursor.execute("SELECT id FROM operations WHERE idempotency_key = ?", (request.idempotency_key,))
    row = cursor.fetchone()
    if row:
        operation_id = row["id"] if isinstance(row, sqlite3.Row) else row[0]
        logger.info({"event": "idempotency_hit", "operation_id": operation_id})
        return {"operation_id": operation_id}

    # Create new operation
    cursor.execute(
        "INSERT INTO operations (idempotency_key, action, payload, status) VALUES (?, ?, ?, ?)",
        (request.idempotency_key, request.action, json.dumps(request.payload), "pending"),
    )
    operation_id = cursor.lastrowid
    conn.commit()

    logger.info({"event": "operation_created", "operation_id": operation_id})
    return {"operation_id": operation_id}

@app.get("/v1/agent/operations/{operation_id}", response_model=OperationStatus)
async def get_operation_status(operation_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, status FROM operations WHERE id = ?", (operation_id,))
    operation = cursor.fetchone()
    conn.close()

    if not operation:
        raise HTTPException(status_code=404, detail="Operation not found")

    logger.info({"event": "operation_status_retrieved", "operation_id": operation_id})
    return {"operation_id": operation["id"], "status": operation["status"]}

@app.post("/operations", response_model=Operation, status_code=200, summary="Create a new operation", description="Creates a new operation with the provided action and payload.")
def create_operation(op: OperationIn):
    try:
        idempotency_key = str(op.idempotency_key) if op.idempotency_key else str(uuid.uuid4())
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO operations (idempotency_key, action, payload, status) VALUES (?, ?, ?, ?)",
            (idempotency_key, op.action, json.dumps(op.payload), "pending"),
        )
        new_id = cursor.lastrowid
        conn.commit()
        return Operation(id=new_id, action=op.action, payload=op.payload, status="pending")
    except Exception as e:
        logger.error("DB insert error", extra={"exception": traceback.format_exc()})
        raise HTTPException(status_code=500, detail=f"DB insert failed: {str(e)}")

@app.post("/operations/{operation_id}/run", response_model=Operation, summary="Run an operation", description="Executes the specified operation and updates its status.")
async def run_operation(operation_id: int):
    try:
        logger.debug("Starting run_operation", extra={"operation_id": operation_id})
        conn = get_db_connection()
        logger.debug("run_operation: acquired connection", extra={"db_conn": repr(conn)})
        cursor = conn.cursor()

        cursor.execute("SELECT id, action, payload FROM operations WHERE id = ?", (operation_id,))
        operation = cursor.fetchone()

        if not operation:
            raise HTTPException(status_code=404, detail="Operation not found")

        logger.debug("Fetched operation details", extra={
            "operation_id": operation_id,
            "operation": operation
        })

        action = operation["action"] if isinstance(operation, sqlite3.Row) else operation[1]
        payload_text = operation["payload"] if isinstance(operation, sqlite3.Row) else (operation[2] if operation else None)
        try:
            payload_obj = json.loads(payload_text) if isinstance(payload_text, str) and payload_text else payload_text or {}
        except Exception:
            payload_obj = payload_text

        # avoid double-wrapping
        if isinstance(payload_obj, dict) and "payload" in payload_obj:
            body_to_send = payload_obj
        else:
            body_to_send = {"payload": payload_obj}

        url = "http://document-service:8081/generate"
        headers = {"Content-Type": "application/json"}

        # Construct the payload
        payload = {"payload": payload_obj}

        # Add structured debug log just before the call
        logger.debug("Outgoing request", extra={
            "url": url,
            "method": "POST",
            "headers": headers,
            "body": json.dumps(payload, sort_keys=True)
        })

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers, timeout=10.0)
                response.raise_for_status()
                result = response.json()
            except httpx.HTTPStatusError as e:
                logger.error("HTTPStatusError", extra={
                    "status_code": e.response.status_code,
                    "response_body": e.response.text
                })
                raise
            except Exception:
                logger.error("Unexpected error during HTTP request", extra={
                    "traceback": traceback.format_exc()})
                raise

        cursor.execute(
            "UPDATE operations SET status = 'done' WHERE id = ?",
            (operation_id,)
        )
        conn.commit()

        return Operation(id=operation_id, action=action, payload=payload_text, status="done", result=result)

    except Exception as e:
        logger.error("Error in run_operation", extra={"exception": traceback.format_exc()})
        raise HTTPException(status_code=500, detail=f"Error running operation: {str(e)}")