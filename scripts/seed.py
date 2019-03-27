#!/usr/bin/env python3
"""Seed script"""

from typing import List, Tuple

from faker import Faker
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from src.database import connect_db

# TODO: kill process after seeding...


def create_dev_server() -> Tuple[SQLAlchemy, dict]:
    """Create an instance of the development server, and seeds the database"""
    app = Flask(__name__)

    # Apply development config to flask app
    app.config.from_object(f"config.DevelopmentConfig")

    # route to handle killing the server
    @app.route('/kill', methods=['POST'])
    def kill_app():
        """Stops the server, or throws an error if we are in the wrong environment."""
        shutdown = request.environ.get('werkzeug.server.shutdown')
        if shutdown is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        shutdown()
        return "Shutting down..."

    # Create and return db connection
    return connect_db(app)


def generate_fake_data(models: dict, size: int) -> List[dict]:
    """Generate input `size` number (or 100) fake projects with associated Items and Options."""
    fake = Faker()

    # all fake data
    fake_data = []

    print("Generating mock data...")

    # 100 (by default) fake projects
    for i in range(size):
        new_project = models["Project"](fake.iban(), fake.email(), fake.phone_number())
        fake_data.append(new_project)

        # 1-18 fake items per project
        for j in range((i % 10 * 2) or 1):
            new_item = models["Item"](new_project.id, fake.uuid4(), new_project.title)
            fake_data.append(new_item)

            # 0-9 fake options per item
            for k in range(1, 10 % (j or 1)):
                fake_data.append(models["Option"](new_project.id, new_item.id, k, fake.image_url()))
                new_item.total_num += 1

    print("Finished generating mock data...")

    return fake_data


def seed_db(seed_num: int = 100) -> None:
    """Seeds the database with 100 fake Projects + Items and Options"""

    # Create a dev server
    db, models = create_dev_server()

    # Generates fake data for Projects, Items and Options
    fake_data = generate_fake_data(models, seed_num)

    # Commit changes to the database
    try:
        print("Adding mock data to database...")
        db.add_all(fake_data)
        print("Committing changes to database...")
        db.commit()
    except:
        print("There was an error during seeding.")
        requests.get('http://example.com')
    finally:
        print("Finished seeding!")
        requests.get('http://example.com')
