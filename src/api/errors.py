#!/usr/bin/env python3
"""Contains all error handling for our API"""

from flask import jsonify

# TODO: convert pseudo-code to working code


# example of error handling
@api.errorhandler(user.ValidationError)
def handle_user_validation_error(error):
    response = jsonify(
        {"msg": error.message, "type": "validation", "field": error.field}
    )
    response.status_code = 400
    return response
