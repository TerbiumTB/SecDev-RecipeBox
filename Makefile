#Common
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

#Docker
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


#CI
ci-test:
	pytest -v --cov=app --cov-report=xml --cov-report=html

ci-lint:
	ruff check --output-format=github .
	black --check .
	isort --check-only .

ci-security:
	bandit -r . -f json -o bandit-report.json || true
	bandit -r . -f html -o bandit-report.html || true
	safety check --json --output safety-report.json || true

ci: ci-lint ci-security ci-test

#DAST
dast-local:
	echo "Starting ZAP baseline scan..."
	mkdir -p EVIDENCE/P11
	docker run --rm --network host -v $$PWD:/zap/wrk ghcr.io/zaproxy/zaproxy:stable \
		zap-baseline.py \
		-t http://localhost:8000/health \
		-r zap_baseline.html \
		-J zap_baseline.json \
		-d || true
	mv zap_baseline.* EVIDENCE/P11/ || true
	echo "ZAP scan completed. Reports saved to EVIDENCE/P11/"

hadolint:
	docker run --rm -i hadolint/hadolint < Dockerfile \
	| tee hadolint_output.txt

chekov:
	docker run --rm -v $PWD:/work bridgecrew/checkov \
		-d /work/iac \
		-o json \
		--compact > EVIDENCE/P12/checkov_report.json

trivy:
	docker build -t myapp:local .

	docker run --rm -v $PWD:/work aquasec/trivy \
	image myapp:local \
		--format json \
		--output /work/EVIDENCE/P12/trivy_report.json
