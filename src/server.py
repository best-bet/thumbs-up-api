#!/usr/bin/env python3
"""
Documentation

See also https://github.com/best-bet/thumbs-up-api

Contains the logic to create an instance of the server
"""

import os

from flask import Flask
from flask_cors import CORS

from .database import connect_db

# TODO: Connect to api


def create_app():
    """Create an instance of the Flask server"""
    app = Flask(__name__)

    # Grab FLASK_ENV and format it into a config name, then add that config to our app
    app.config.from_object(f"config.{str.capitalize(os.environ['FLASK_ENV'])}Config")

    # Create db connection
    db, models = connect_db(app)

    # Setup CORS headers to allow all domains
    CORS(app)

    @app.route("/")
    def root():
        """possibly temporary route / debugging route"""
        return f"<div>app root</div>"

    @app.route("/api/")
    def api():
        """How to run this"""

        # TODO: connect api

        # connect to api.projects here...
        return "<h1>api</h1>"

    @app.route("/api/projects/<id>")
    def api():
        """test"""

        project = models["Project"].query(1)

        return f"<h1>{project.email}</h1>"

    return app
