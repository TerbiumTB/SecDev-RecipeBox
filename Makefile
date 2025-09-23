pr-ritual:
	ruff check --fix .
	black .
	isort .
	pytest -q
	pre-commit run --all-files
