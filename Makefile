# Makefile para el proyecto PUPIBOT

.PHONY: dev-install test

dev-install:
	source .venv/bin/activate && pip install -r requirements-dev.txt

test:
	source .venv/bin/activate && pytest -v