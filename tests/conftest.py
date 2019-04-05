#!/usr/bin/env python3
"""Context for running tests"""

import pytest
from flask import Flask

from src import create_app, connect_db, Item, Project, Option


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  -------------------------- * FIXTURES * ---------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@pytest.fixture(scope='module')
def app():
    """Test server"""

    # Instance of Flask server for test suite
    app = create_app()

    # Grab FLASK_ENV and format it into a config name, then add that config to our app
    app.config.from_object("config.TestConfig")

    return app


@pytest.fixture(scope='module')
def test_client(app: Flask):
    """Use Flask's testing client as a fixture for test suite."""

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


@pytest.fixture(scope='module')
def test_database(app: Flask):
    """Initializes database for testing purposes."""

    # Create the database and the database table
    db_session = connect_db(app)
    # db_session.create_all()

    yield db_session, {"Project": Project, "Item": Item, "Option": Option}

    # db_session.drop_all()


@pytest.fixture(scope='module')
def new_project(test_database):
    """New project fixture"""

    db_session, models = test_database

    title = "Lord of the Rings"
    email = "J. R. R. Tolkien"
    phone = "5558675309"

    yield models["Project"](title=title, email=email, phone=phone)


@pytest.fixture(scope='module')
def new_item(test_database, new_project):
    """New item fixture"""

    db_session, models = test_database

    item_id = "1"

    yield models["Item"](project_id=new_project.id, item_id=item_id)


@pytest.fixture(scope='module')
def test_option(test_database, new_project, new_item):
    """New option fixture"""

    db_session, models = test_database

    option_num = "1"
    content = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Walrus_(Odobenus_rosmarus)_on_Svalbard.jpg/1920px-Walrus_(Odobenus_rosmarus)_on_Svalbard.jpg"

    yield models["Option"](project_id=new_project.id, item_id=new_item.id, option_num=option_num, content=content)
