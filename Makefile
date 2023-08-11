.PHONY: build up lint down

build:
	docker compose build

up:
	docker compose up -d

lint:
	docker compose exec app pylint *.py

down:
	docker compose down

restart:
	docker compose restart