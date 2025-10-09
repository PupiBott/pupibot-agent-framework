from fastapi import FastAPI

from services.agent_runner.src.api import tools

app = FastAPI(title="Agent Runner")
app.include_router(tools.router)
