#!/usr/bin/env python3
"""Contains validation logic for models"""


# possible error for projects --- if wrong info is provided
class ValidationError(Exception):
    def __init__(self, field, message):
        self.field = field
        self.message = message
