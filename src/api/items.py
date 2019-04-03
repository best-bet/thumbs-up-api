#!/usr/bin/env python3
"""RESTful items route, contains routes for POST, PATCH, and DELETE."""

import json
import pickle

from flask import Blueprint, request
from sqlalchemy.orm import scoped_session
from slots import MAB

# from .decorators import background, email, limit
from .utils import find_project_item_option, update_item
from ..database import Item, Option
from ..utils import hash_id

# TODO: handle POST case where item already exists (id)
# TODO: MAB logic in item PATCH route
# TODO: error handle --- item id invalid, etc.
# TODO: implement decorators
# TODO: email project owner that a trial has completed


def items_api_route(db_session: scoped_session) -> Blueprint:
    """Wrapper for items Blueprint for passing db connection."""

    # Blueprint for projects
    items = Blueprint("items", __name__, url_prefix="/api/items")

    # ***********************
    #  GET --- GET NEXT ITEM
    # ***********************
    @items.route("/", methods=["GET"])
    def create_item():
        """GET - get the next option in line for the given item."""

        # Extract token and id from request body
        token = request.form.get("token")
        item_id = request.form.get("item_id")

        # Find project by token and item by id
        query_data = find_project_item_option(token=token, item_id=item_id)
        if "error" in query_data:
            return query_data["error"]

        res = {
            "url": query_data["item"].next,
            "send_data": query_data["item"].active_trial
        }

        return json.dumps(res)

    # **********************
    #  POST --- CREATE ITEM
    # **********************
    @items.route("/", methods=["POST"])
    # @limit(requests=100, window=(24 * 60 * 60 * 1000), by="ip")  # limit: 100 requests per day by ip
    def create_item():
        """POST - create an item given an `project_token` and `item_id`."""

        # Extract token and id from request body
        token = request.form.get("token")
        item_id = request.form.get("item_id")

        # Find project by token
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

    # **********************************
    #  PATCH --- INITIALIZE MAB ON ITEM
    # **********************************
    # @email
    @items.route("/", methods=["PATCH"])
    def initialize_mab() -> str:
        """Initialize the multi-armed bandit for an item, and update item's row with the MAB test class instance."""

        # how will this one be hit alone?

        # Extract token and id from request body
        token = request.form.get("token")
        item_id = request.form.get("item_id")

        # Find project by token and item by id
        query_data = find_project_item_option(token=token, item_id=item_id)
        if "error" in query_data:
            return query_data["error"]

        if query_data["item"].mab:
            return "This trial has already begun."

        # ......
        pickled_mab = pickle.dumps(MAB(num_bandits=query_data["item"].total_num))
        query_data["item"].mab = pickled_mab
        query_data["item"].active_trial = True

        try:
            db_session.add(query_data["item"].mab)
            db_session.commit()
        except:
            return "500 - internal server error."

        return "MAB successfully initiated, trials are ready to begin!\n\nYou can no longer add, or delete options. You must delete this item if you wish to make changes."

    # ***********************
    #  PATCH --- UPDATE ITEM
    # ***********************
    # @email
    @items.route("/", methods=["PATCH"])
    # @background
    def next_item() -> str:
        """PATCH - retrieve the next option in line, and replace that with the following option."""

        # Extract token, item_id, option_num and clicked from request body
        token = request.form.get("token")
        item_id = request.form.get("item_id")
        option_num = request.form.get("option_num")  # with GET, send what number option was used
        clicked = int(request.form.get("clicked"))  # bool converted to 0 or 1

        # Find project by token and item by id
        query_data = find_project_item_option(token=token, item_id=item_id)
        if "error" in query_data:
            return query_data["error"]

        # Break if the trial has not yet started
        if not query_data["item"].mab:
            return "This trial has not yet begun. Please start the trial to continue."

        # Break if the trial has already ended.
        if not query_data["item"].active_trial:
            return "This trial has already ended."

        mab = pickle.loads(query_data["item"].mab)
        trial_results = mab.online_trial(bandit=option_num, payout=clicked, strategy='bayesian')

        # Update database with trial results
        res = update_item(query_data, trial_results, mab)

        return res

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

        # Find project by token and item by id
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
