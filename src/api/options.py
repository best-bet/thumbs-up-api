#!/usr/bin/env python3
"""RESTful options route, contains routes for POST and DELETE."""

from flask import Blueprint, request
from sqlalchemy.orm import scoped_session

# from .decorators import background, email, limit
from .utils import find_project_item_option
from ..database import Option
from ..utils import hash_id, Validate

# TODO: if option is first option on an item, set item's next to that value
# TODO: MAB logic in option delete
# TODO: error handle --- option invalid, etc.
# TODO: implement decorators


def options_api_route(db_session: scoped_session) -> Blueprint:
    """Wrapper for projects Blueprint, passes db connection to routes."""

    # Blueprint for projects
    options = Blueprint("options", __name__, url_prefix="/api/options")

    # ************************
    #  POST --- CREATE OPTION
    # ************************
    @options.route("/", methods=["POST"])
    # @limit(requests=100, window=(24 * 60 * 60 * 1000), by="ip")  # limit: 100 requests per day by ip
    def create_option():
        """POST - create an option given a `token`, `item_id` and `content`."""

        # Extract token, item_id and content from request body
        token = request.form.get("token")
        item_id = request.form.get("item_id")
        content = request.form.get("content")

        if not Validate.url(content):
            return "Content invalid."

        # Find project by token and item by id
        query_data = find_project_item_option(token=token, item_id=item_id)
        if "error" in query_data:
            return query_data["error"]

        try:
            # Create a new project from the query params
            new_option = Option(
                project_id=query_data["project"].id,
                item_id=item_id,
                option_num=query_data["item"].total_num,
                content=content,
            )
            db_session.add(new_option)
            db_session.commit()
        except:
            return "500 - internal server error."

        return f"<h1>content={new_option.content}, id={new_option.id}</h1>"  # not this

    # **************************
    #  DELETE --- DELETE OPTION
    # **************************
    @options.route("/", methods=["DELETE"])
    # @limit(requests=100, window=(24 * 60 * 60 * 1000), by="ip")  # limit: 100 requests per day by ip
    def delete_option() -> str:
        """DELETE - delete an option given the content associated with the option."""

        # Extract token, item_id and option_content from request body
        token = request.form.get("token")
        item_id = request.form.get("item_id")
        option_content = request.form.get("option_content")

        # Find project by token and item by id
        query_data = find_project_item_option(token=token, item_id=item_id)
        if "error" in query_data:
            return query_data["error"]

        # Check each option for a match with option content
        for i in range(1, query_data["item"].total_num + 1):
            option_id = hash_id(query_data["project"].id, item_id, i)
            option = Option.query(option_id)
            if option.content == option_content:
                # Delete right away if the match is the last item
                if i == query_data["item"].total_num:
                    db_session.delete(option)
                # Swap option with the last option, and delete new last option
                else:
                    last_option_id = hash_id(query_data["project"].id, item_id, query_data["item"].total_num)
                    last_option = Option.query(last_option_id)
                    last_option.id = option.id
                    db_session.add(last_option)
                    db_session.delete(option)

                # Decrement the number of options associated with item
                query_data["item"].total_num -= 1
                db_session.add(query_data["item"].total_num)

                if query_data["item"].next == option_content:
                    # do some MAB magic and find the next value
                    pass

                try:
                    # Commit changes to the database
                    db_session.commit()
                    return "Content successfully deleted."
                except:
                    return "500 - internal server error."

            # If there was no match
            return "Content was not a match."

    # Return options Blueprint
    return options
