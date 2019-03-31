#!/usr/bin/env python3
"""
Contains the logic to create an instance of the server

See also https://github.com/best-bet/thumbs-up-api
"""

import os

from flask import Flask, g, jsonify, request
from flask_cors import CORS

from .api import projects, items, options
from .database import connect_db

# TODO: Connect to api


def create_app():
    """Create an instance of the Flask server"""
    app = Flask(__name__)

    # Grab FLASK_ENV and format it into a config name, then add that config to our app
    app.config.from_object(f"config.{str.capitalize(os.environ['FLASK_ENV'])}Config")

    # Create db connection
    db_session = connect_db(app)

    # Register blueprints
    app.register_blueprint(projects(db_session))
    app.register_blueprint(items(db_session))
    app.register_blueprint(options(db_session))

    # Setup CORS headers to allow all domains
    CORS(app)

    @app.route("/")
    def root():
        """possibly temporary route / debugging route"""
        return f"<div>app root</div>"

    # try to rate limit things the user wont need a lot of
    @app.after_request
    def inject_rate_limit_headers(response):
        try:
            requests, remaining, reset = map(int, g.view_limits)
        except (AttributeError, ValueError):
            return response
        else:
            h = response.headers
            h.add('X-RateLimit-Remaining', remaining)
            h.add('X-RateLimit-Limit', requests)
            h.add('X-RateLimit-Reset', reset)
            return response

    @app.errorhandler(404)
    def not_found(error=None):
        """404 - Resource not found."""

        # Error response
        message = {"status": 404, "message": "Not Found: " + request.url}

        resp = jsonify(message)
        resp.status_code = 404

        return resp

    return app
