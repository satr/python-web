SHELL := /bin/bash

.PHONY: run-api-local
run-api-local:
	cd ./api/src && ../.venv/bin/uvicorn main:app --reload

.PHONY: run-flask-app-local
run-flask-app-local:
	cd ./flask-app/src && ../.venv/bin/flask run --host 0.0.0.0 --port 8001 --reload

.PHONY: run-flask-app-local
run-flask-app-local:
	cd ./flask-app/src && ../.venv/bin/uvicorn main:app --reload


