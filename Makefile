
start:
	docker-compose up -d --build --remove-orphans

stop:
	docker-compose down --volumes --remove-orphans

db:
	docker run --rm -d -p 5432:5432 -e POSTGRES_USER=dbuser -e POSTGRES_PASSWORD=dbpassword -e POSTGRES_DB=dbname postgres:15.1-alpine

server:
	cd src && python main.py

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev

install:
	pip install -r requirements.txt

test:
	pytest --no-header -vv

test-in-docker:
	docker-compose -f docker-compose-test.yml up --build --exit-code-from web-app-test --remove-orphans

isort:
	isort src

worker:
	poetry run celery -A app.app_tasks.tasks worker -B -l info -Q sync_db_with_excel -c 1

pycache:
	poetry run pyclean -v .

bot:
	PYTHONPATH=$(PWD)/src python3 src/bot/main.py

stop-bot:
	-ps aux | grep bot/main.py | grep -v grep | awk '{print $$2}' | xargs -r kill -2 || true



