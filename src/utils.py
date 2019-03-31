#!/usr/bin/env python3
"""Utility functions, includes: `hash_id` and Validate class"""

import re


def hash_id(*args: str or int) -> str:
    """A simple hashing function to generate `id`s given any number of string or number inputs."""
    return ":".join([str(val) for val in args])


class Validate:
    @staticmethod
    def email(x: str) -> bool:
        """Use regular expressions to check if input string is a valid email."""
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        try:
            return len(re.match(regex, x).groups()) == 1
        except:
            return False

    @staticmethod
    def phone(x: str) -> bool:
        """Use regular expressions to check if input string is a valid phone number."""
        regex = r"(\d{3}[-\s]??\d{3}[-\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\s]??\d{4}|\d{3}[-\s]??\d{4})"
        try:
            return len(re.match(regex, x).groups()) == 1
        except:
            return False

    @staticmethod
    def title(x: str) -> bool:
        """Use regular expressions to check if input string is a valid project title."""
        regex = r"^(?![-._])(?!.*[_.-]{2})[\w.-]{6,30}(?<![-._])$"
        try:
            return re.match(regex, x) is not None
        except:
            return False

    @staticmethod
    def url(x: str) -> bool:
        """Use regular expressions to check if input string is a valid url."""
        regex = r"(^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$)"
        try:
            return len(re.match(regex, x).groups()) == 1
        except:
            return False
