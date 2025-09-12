SHELL := /bin/bash

CR_URL ?= ghcr.io/satr/python-web-
PLATFORM ?= linux/arm64

.PHONY: run-api-local
run-api-local:
	cd ./api/src && ../.venv/bin/uvicorn main:app --reload

.PHONY: run-mq
run-mq:
	docker run -it -p 5672:5672 -p 15672:15672 --name rabbitmq --rm rabbitmq:3-management

.PHONY: build-api-docker
build-api-docker:
	docker build --platform=$(PLATFORM) ./api -t $(CR_URL)python-api:latest

.PHONY: run-api-docker
run-api-docker: build-api-docker
	docker run -it -p 5672:5672 -p 15672:15672 --name rabbitmq --rm rabbitmq:3-management
	docker run -p 8000:8000 $(CR_URL)python-api:latest

.PHONY: build-flask-app-docker
build-flask-app-docker:
	docker build --platform=$(PLATFORM) ./flask-app -t $(CR_URL)python-flask-app:latest

.PHONY: run-flask-app-docker
run-flask-app-docker: build-flask-app-docker
	docker run -it -p 5672:5672 -p 15672:15672 --name rabbitmq --rm rabbitmq:3-management
	docker run -p 8001:8001 $(CR_URL)python-flask-app:latest

.PHONY: build-order-processor-docker
build-order-processor-docker:
	docker build --platform=$(PLATFORM) ./jobs/order_processor -t $(CR_URL)python-order-processor:latest

.PHONY: run-order-processor-docker
run-order-processor-docker: build-order-processor-docker
	docker run -it -p 5672:5672 -p 15672:15672 --name rabbitmq --rm rabbitmq:3-management
	docker run $(CR_URL)python-order-processor:latest

.PHONY: run-flask-app-local
run-flask-app-local:
	cd ./flask-app/src && ../.venv/bin/flask run --host 0.0.0.0 --port 8001 --reload

.PHONY: push-api-docker
push-api-docker: build-api-docker
	docker push $(CR_URL)python-api:latest

.PHONY: push-flask-app-docker
push-flask-app-docker: build-flask-app-docker
	docker push $(CR_URL)python-flask-app:latest

.PHONY: push-order-processor-docker
push-order-processor-docker: build-order-processor-docker
	docker push $(CR_URL)python-order-processor:latest

.PHONY: push-docker-all
push-docker-all: push-api-docker push-flask-app-docker push-order-processor-docker

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
