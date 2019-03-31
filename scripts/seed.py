#!/usr/bin/env python3
"""Script for seeding the database with mock data."""

import sys
from typing import List, Tuple

from faker import Faker
from flask import Flask, request
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session

from src.database import connect_db, Project, Item, Option

# TODO: kill process after seeding.
# TODO: pass `SEED_NUM` from terminal to `seed_db` as argument.


def create_dev_server() -> Tuple[Flask, scoped_session]:
    """Create an instance of the development server, and seeds the database"""

    # Start dev-server
    app = Flask(__name__)

    # Apply development config to flask app
    app.config.from_object(f"config.DevelopmentConfig")

    # route to handle killing the server
    @app.route("/kill", methods=["POST"])
    def kill_app():
        """Stops the server, or throws an error if we are in the wrong environment."""
        shutdown = request.environ.get("werkzeug.server.shutdown")
        if shutdown is None:
            raise RuntimeError("Not running with the Werkzeug Server")
        shutdown()
        return "Shutting down..."

    # Create db connection and register models
    db_session = connect_db(app)

    return app, db_session


def generate_fake_data(size: int) -> List[Project and Item and Option]:
    """Generate input `size` number (or 100) fake projects with associated Items and Options."""
    fake = Faker()

    # all fake data
    fake_data = []

    print("Generating mock data...")

    # 100 (by default) fake projects
    for i in range(size):
        new_project = Project(
            title=fake.iban(), email=fake.email(), phone=fake.phone_number()
        )
        fake_data.append(new_project)

        # 1-18 fake items per project
        for j in range((i % 10 * 2) or 1):
            new_item = Item(
                project_id=new_project.id,
                item_id=fake.uuid4()
            )
            fake_data.append(new_item)

            # 0-9 fake options per item
            for k in range(1, 10 % (j or 1)):
                fake_data.append(
                    Option(
                        project_id=new_project.id,
                        item_id=new_item.id,
                        option_num=k,
                        content=fake.image_url(),
                    )
                )
                new_item.total_num += 1

    print("Finished generating mock data...")

    return fake_data


def seed_db(seed_num: int = 100) -> Flask:
    """Seeds the database with 100 fake Projects + Items and Options"""

    # Create a dev server
    app, db_session = create_dev_server()

    # Generates fake data for Projects, Items and Options
    fake_data = generate_fake_data(seed_num)

    # Commit changes to the database
    try:
        print("Adding mock data to database...")
        db_session.add_all(fake_data)

        print("Committing changes to database...")
        db_session.commit()

        print("Changes Committed to database!")
        print("Finished seeding!")

    except SQLAlchemyError as err:
        print("There was a SQLAlchemy error during seeding.", err, file=sys.stderr)

    except:
        print("Uncaught error:", sys.exc_info()[0], file=sys.stderr)

    finally:
        db_session.close()
        print("Kill server, seeding is complete.")
        # kill server

    return app
