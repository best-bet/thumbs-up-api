#!/usr/bin/env python3
"""RESTful items route, contains routes for POST, PATCH, and DELETE."""

from flask import Blueprint, request
from sqlalchemy.orm import scoped_session

# from .decorators import background, email, limit
from .utils import find_project_item_option
from ..database import Item, Option
from ..utils import hash_id

# TODO: handle POST case where item already exists (id)
# TODO: MAB logic in item PATCH route
# TODO: error handle --- item id invalid, etc.
# TODO: implement decorators


def items_api_route(db_session: scoped_session) -> Blueprint:
    """Wrapper for items Blueprint for passing db connection."""

    # Blueprint for projects
    items = Blueprint("items", __name__, url_prefix="/api/items")

    # **********************
    #  POST --- CREATE ITEM
    # **********************
    @items.route("/", methods=["POST"])
    # @limit(requests=100, window=(24 * 60 * 60 * 1000), by="ip")  # limit: 100 requests per day by ip
    # @email
    def create_item():
        """POST - create an item given an `project_token` and `item_id`."""

        # Extract token and id from request body
        token = request.form.get("token")
        item_id = request.form.get("item_id")

        query_data = find_project_item_option(token=token)
        if "error" in query_data:
            return query_data["error"]

        try:
            # Create a new project from the query params
            new_item = Item(project_id=query_data["project"].id, item_id=item_id)
            db_session.add(new_item)
            db_session.commit()
        except:
            db_session.rollback()
            return "500 - internal server error."

        return f"<h1>id={new_item.id}, total_num={new_item.total_num}</h1>"  # not this

    # ***********************
    #  PATCH --- UPDATE ITEM
    # ***********************
    @items.route("/", methods=["PATCH"])
    # @background
    def next_item() -> str:
        """PATCH - retrieve the next option in line, and replace that with the following option."""

        # Extract token and id from request body
        token = request.form.get("token")
        item_id = request.form.get("item_id")

        query_data = find_project_item_option(token=token, item_id=item_id)
        if "error" in query_data:
            return query_data["error"]

        # next option in line --- value to be returned
        next_option = query_data["item"].next

        # replace item.next with MAB here...

        return next_option

    # ************************
    #  DELETE --- DELETE ITEM
    # ************************
    @items.route("/", methods=["DELETE"])
    # @limit(requests=100, window=(24 * 60 * 60 * 1000), by="ip")  # limit: 100 requests per day by ip
    def delete_item() -> str:
        """DELETE - delete a project and all associated data given a `token`."""

        # Extract token and id from request body
        token = request.form.get("token")
        item_id = request.form.get("item_id")

        query_data = find_project_item_option(token=token, item_id=item_id)
        if "error" in query_data:
            return query_data["error"]

        # Iterate through all of the options related to the item and delete them
        for i in range(1, query_data["item"].total_num + 1):
            option = Option.query.get(hash_id(query_data["project"].id, item_id, i))
            db_session.delete(option)

        try:
            db_session.delete(query_data["item"])
            db_session.commit()
        except:
            db_session.rollback()
            return "500 - internal server error."

        return f"Item with id of {item_id} and all related data was successfully deleted."

    # Return items Blueprint
    return items
