#!/usr/bin/env python3
"""Blueprints for api routes: `projects`, `items` and `options`."""

from .projects import projects_api_route
from .items import items_api_route
from .options import options_api_route


__all__ = ["projects", "items", "options"]

projects = projects_api_route
items = items_api_route
options = options_api_route
