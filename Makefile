ifneq (,$(wildcard ./.env))
    include .env
    export
endif

init:
	pip install -r requirements-dev.txt
	pre-commit install

lint:
	ruff check --fix .
	black .
	isort .

test:
	pytest -q

coverage:
	pytest --cov=app tests/

check: lint test
	pre-commit run --all-files

run:
	uvicorn app.main:app --reload
