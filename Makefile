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

local:
	uvicorn app.main:app --reload

build:
	docker-compose build --no-cache

stop:
	docker-compose down

clean:
	docker-compose down -v --remove-orphans

run:
	docker-compose up -d

rerun: | stop run

start: | build run

restart: | stop start

fresh: | clean start
