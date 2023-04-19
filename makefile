up:
		docker-compose up -d --build

stop:
		docker-compose stop

down:
		docker-compose down

reformat:
	black .
	isort .
	flake8
	mypy ./app
	mypy ./tests


lint:
	black --check .
	isort --check-only .
	flake8
	mypy ./app
	mypy ./tests

test: up
	export TEST_MODE=1
	pytest -v
	docker-compose down