#!/usr/bin/env python3
"""utility functions, includes: `hash_id`"""


def hash_id(*args: str) -> str:
    """A simple hasing function to generate `id`s given any number of string or number inputs."""
    return ":".join([str(val) for val in args])
