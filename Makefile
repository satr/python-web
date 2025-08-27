SHELL := /bin/bash

.PHONY: run-api-local

run-api-local:
	uvicorn api.src.main:app --reload


