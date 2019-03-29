#!/usr/bin/env python3
"""Database declaration file"""

from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# TODO: flask_migrate wont work because we are using raw sqlalchemy instead of flask_sqlalchemy, find a replacement


# Declare in module's scope to import in .models
Base = declarative_base()


def connect_db(app: Flask) -> scoped_session:
    """Create a connection to the database, migrate changes and register the models."""

    # Connect to database
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"], convert_unicode=True)

    # Bind session to db connection --- this is connection used by API
    db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

    # Create Base query and Base metadata
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)

    # Migrate changes in schema into database
    Migrate(app, engine)

    # Register models
    from .models import Project, Item, Option

    return db_session
