init:
	pip install -r requirements.txt

lint:
	ruff check --fix .
	black .
	isort .

test:
	pytest -q

coverage:
	pytest --cov=app tests/

check: lint test

run:
	uvicorn app.main:app --reload
