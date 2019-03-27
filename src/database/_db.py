#!/usr/bin/env python3
"""Database declaration file"""

from typing import Tuple

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from .models import register_models

# TODO: Fix error with GUID during migration


def connect_db(app: Flask) -> Tuple[SQLAlchemy, dict]:
    """Create an instance of the database and connect it to the app."""
    database = SQLAlchemy(app)

    # Migrate changes in schema into database
    Migrate(app, database)

    # Pass the new connection to the db to register the models with the db
    models = register_models(database)

    return database, models
