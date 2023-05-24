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

lint:
	black .
	isort .
	flake8
	mypy ./app
	mypy ./tests


check:
	black --check .
	isort --check-only .
	flake8
	mypy ./app
	mypy ./tests

test:
	docker-compose up -d localstack
	pytest -vv -s
	docker-compose down

test_local: lint
	docker-compose up -d localstack && bash -c 'source .env && export $$(cut -d= -f1 .env) && pytest -vv -s' && docker-compose down

build_image:
	docker build --target prod -t petrishutin/filestorage:latest .

push_image: build_image
	docker login
	docker push petrishutin/filestorage:latest

login_gar:
	docker login us-central1-docker.pkg.dev/august-gradient-382709/repo1
