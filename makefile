up:
		docker-compose up -d --build

stop:
		docker-compose stop

down:
		docker-compose down

lint:
	black .
	isort .
	black --check .
	isort --check-only .
	flake8
	mypy ./app
	mypy ./tests

test: up
	pytest -v
	docker-compose down