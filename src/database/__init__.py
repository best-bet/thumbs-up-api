# this file designates `db/` as a package
"""Package contains `connect_db` a function that passes the instance of app to connect to the db."""

from ._db import connect_db
from .models import Project, Item, Option

__all__ = ["connect_db", "Project", "Item", "Option"]
