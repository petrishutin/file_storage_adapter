deps:
		pip install --upgrade pip
		pip install -r requirements.txt
		pip install -r requirements-dev.txt

up:
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
	docker-compose up -d localstack
	pytest -vv -s
	docker-compose down