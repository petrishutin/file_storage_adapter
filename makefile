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
	FILE_STORAGE_SERVICE=S3FileStorage
	pytest -v
	FILE_STORAGE_SERVICE=LocalFileStorage
	pytest -v
	docker-compose down