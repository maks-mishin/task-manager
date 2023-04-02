MANAGE := poetry run python manage.py

run:
	@$(MANAGE) runserver

test:
	@$(MANAGE) test -v 2

setup: db-clean install migrate

install:
	@poetry install

db-clean:
	@rm db.sqlite3 || true

migrate:
	@$(MANAGE) makemigrations
	@$(MANAGE) migrate

shell:
	@$(MANAGE) shell_plus --ipython

lint:
	@poetry run isort task_manager users labels tasks statuses
	@poetry run flake8 task_manager users labels tasks statuses

trans:
	@poetry run django-admin makemessages --ignore="static" --ignore=".env" --ignore="venv" --ignore="migrations" -l en
	@poetry run django-admin compilemessages

super:
	@poetry run python manage.py createsuperuser