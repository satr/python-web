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


.PHONY: gen-api-client
gen-api-client:
	echo "run API" && cd ./flask-app/src && mkdir -p app/clients/fast_api; ../.venv/bin/openapi-python-client generate --url http://localhost:8000/openapi.json --output-path=app/clients/fast_api --overwrite && cd ./app/clients/fast_api && pip install -e .
