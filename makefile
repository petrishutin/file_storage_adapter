deps:
		pip install --upgrade pip
		pip install -r requirements.txt
		pip install -r requirements-dev.txt

up:
	export TEST_MODE=1
	docker-compose up --build

stop:
	docker-compose stop

down:
	docker-compose down

rebuild:
	docker-compose up -d --build app

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

test:
	export TEST_MODE=1
	docker-compose up localstack
	pytest -vv -s
	docker-compose down