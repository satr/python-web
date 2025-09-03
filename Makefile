SHELL := /bin/bash

.PHONY: run-api-local
run-api-local:
	cd ./api/src && ../.venv/bin/uvicorn main:app --reload

.PHONY: run-api-docker
run-api-docker: run_mq
	docker build ./api -t api && docker run -p 8000:8000 api

.PHONY: run-flask-app-local
run-flask-app-local:
	cd ./flask-app/src && ../.venv/bin/flask run --host 0.0.0.0 --port 8001 --reload

.PHONY: gen-api-client-for-flask-app
gen-api-client-for-flask-app:
	CURRENT_DIR=$$(pwd)
	echo "first run API with MQ"
	docker compose -f docker-compose-api-mq.yml up
	cd ./flask-app
	mkdir -p src/app/clients/fast_api
	.venv/bin/openapi-python-client generate --url http://localhost:8000/openapi.json --output-path=src/app/clients/fast_api --overwrite
	cd "$$CURRENT_DIR"
	unset CURRENT_DIR
	docker compose down

.PHONY: gen-api-client-for-order-processor
gen-api-client-for-order-processor:
	CURRENT_DIR=$$(pwd); echo "first run API" && cd ./jobs/order_processor && mkdir -p src/app/clients/fast_api; .venv/bin/openapi-python-client generate --url http://localhost:8000/openapi.json --output-path=src/app/clients/fast_api --overwrite; cd "$$CURRENT_DIR"; unset CURRENT_DIR

.PHONY: run-mq
run-mq:
	docker run -it -p 5672:5672 -p 15672:15672 --name rabbitmq --rm rabbitmq:3-management
