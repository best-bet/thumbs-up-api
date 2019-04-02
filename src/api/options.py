#!/usr/bin/env python3
"""RESTful options route, contains routes for POST and DELETE."""

from flask import Blueprint, request
from sqlalchemy.orm import scoped_session

# from .decorators import background, email, limit
from .utils import find_project_item_option
from ..database import Option
from ..utils import hash_id, Validate

# TODO: if option is deleted, check if that option is item.next, and if so, find new item.next
# TODO: if option is deleted, and it is the only option, swap out item.next with default content
# TODO: error handle --- option invalid, etc.
# TODO: implement decorators
# TODO: check for duplicate urls associated with the same item upon creation


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

        # Update number of options for item
        query_data["item"].total_num += 1

        # If this is the first option, swap out default value for item.next with new option's content
        if query_data["item"].total_num == 1:
            query_data["item"].next = content

        try:
            # Create a new option from the query params, update item.total_num
            new_option = Option(
                project_id=query_data["project"].id,
                item_id=item_id,
                option_num=query_data["item"].total_num,
                content=content,
            )
            db_session.add_all([new_option, query_data["item"]])
            db_session.commit()
        except:
            db_session.rollback()
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
        content = request.form.get("content")

        # Verify that content is valid before searching
        if not Validate.url(content):
            return "Content invalid."

        # Find project by token and item by id
        query_data = find_project_item_option(token=token, item_id=item_id)
        if "error" in query_data:
            return query_data["error"]

        # Check each option for a match with option content
        for i in range(1, query_data["item"].total_num + 1):
            option = Option.query.get(hash_id(query_data["project"].id, item_id, i))
            if option.content == content:
                # If match is the last option, delete right away
                if i == query_data["item"].total_num:
                    db_session.delete(option)
                # Else, copy data from last to current, and delete the last
                else:
                    last_option_id = hash_id(query_data["project"].id, item_id, query_data["item"].total_num)
                    last_option = Option.query.get(last_option_id)

                    for key in option.__dict__.keys():
                        if key != "id" and key != "_sa_instance_state":
                            setattr(option, key, getattr(last_option, key))

                    db_session.add(option)
                    db_session.delete(last_option)

                # Decrement the number of options associated with item
                query_data["item"].total_num -= 1
                db_session.add(query_data["item"])

                if query_data["item"].next == content:
                    # do some MAB magic and find the next value
                    pass

                try:
                    # Commit changes to the database
                    db_session.commit()
                    return "Content successfully deleted."
                except:
                    db_session.rollback()
                    return "500 - internal server error."

        # If there was no match
        return "Content was not a match."

    # Return options Blueprint
    return options
