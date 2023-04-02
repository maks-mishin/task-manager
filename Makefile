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
	@poetry run isort task_manager
	@poetry run flake8 task_manager

trans:
	@poetry run django-admin makemessages --ignore="static" --ignore=".env" --ignore="venv" -l en
	@poetry run django-admin compilemessages

super:
	@poetry run python manage.py createsuperuser