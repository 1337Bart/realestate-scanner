.PHONY: run-scrape calculate-predictions

run-scrape:
	python3 realestate_scanner/manage.py scrape_listings

calculate-predictions:
	python3 realestate_scanner/manage.py calculate_predictions

start-psql:
	psql -U realestate2 -d realestate2 -h localhost -p 5432

migrate:
	python3 realestate_scanner/manage.py makemigrations realestate_app
	python3 realestate_scanner/manage.py migrate

django-shell:
	python3 realestate_scanner/manage.py shell

create-superser:
	python3 realestate_scanner/manage.py createsuperuser

run-app:
	python3 realestate_scanner/manage.py runserver

create-db:
	sudo -u postgres psql

	CREATE USER realestate2 WITH PASSWORD 'realestate2';
	CREATE DATABASE realestate2 WITH OWNER realestate2;
	GRANT ALL PRIVILEGES ON DATABASE realestate2 TO realestate2;

	psql -U realestate2 -d realestate2 -h localhost -p 5432



start-scraping-endpoint:
	curl -X POST http://127.0.0.1:8000/realestate/start-scraping/ -H "Content-Type: application/json" -d '{"building_type": "mieszkanie", "region": "mazowieckie", "transaction_type": "sprzedaz", "max_pages": 7}'

start-calculation-endpoint:
	curl http://127.0.0.1:8000/realestate/calculate-predictions/

get-listings-endpoint:
	curl http://127.0.0.1:8000/realestate/price-predictions/?city=Katowice&ordering=listing__price


# inside psql
create-unacent-extension:
	CREATE EXTENSION IF NOT EXISTS unaccent;
