HOST=127.0.0.1
TEST_PATH=./
MESSAGE=""

.PHONY: help
help:
	@echo "  init         to install requirements"
	@echo "  db-init      to make db"
	@echo "  seed         to seed db with mock data"
	@echo "  run          to run flask server in development"
	@echo "  run-prod     to run flask server in production"
	@echo "  run-test     to run tests on flask server"
	@echo "  freeze       to make/overwrite requirements.txt"
	@echo "  format       to format code"
	@echo "  lint         to check for linting errors"
	@echo "  clean-pyc    to remove all .pyc and .pyo files"
	@echo "  clean-build  to remove builds"
	@echo "  stage        to stage app for Heroku"
	@echo "  deploy       to deploy app to Heroku"
	@echo "  migrate      to migrate changes to the db, to add a message: MESSAGE=\"'my message'\""

init:
		pip install -r requirements.txt

db-init:
		flask db init

seed:
		FLASK_APP=scripts.seed:seed_db flask run --no-reload

run:
		FLASK_ENV=development FLASK_APP=src:create_app flask run

run-prod:
		FLASK_ENV=production FLASK_APP=src:create_app flask run

run-test:
		FLASK_ENV=test FLASK_APP=tests.__main__:run_suite flask run

freeze:
		pip freeze > requirements.txt

format:
		black ./

lint:
		flake8 --exclude=.tox

clean-pyc:
		find . -name '*.pyc' -exec rm --force {} +
		find . -name '*.pyo' -exec rm --force {} +
		name '*~' -exec rm --force {}

clean-build:
		rm --force --recursive build/
		rm --force --recursive dist/
		rm --force --recursive *.egg-info

stage:
		heroku config:set APP_SETTINGS=config.StagingConfig --remote stage
		heroku run python src/server.py --app thumbs-up-api-stage

deploy:
		heroku config:set APP_SETTINGS=config.ProductionConfig --remote pro
		heroku run python src/server.py --app thumbs-up-api-pro

migrate:
		flask db migrate -m ${MESSAGE}
		flask db upgrade
