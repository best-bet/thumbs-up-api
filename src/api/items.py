#!/usr/bin/env python3
"""RESTful items route, contains routes for POST, PATCH, and DELETE."""

import json
import pickle
import random

from flask import Blueprint, request
from sqlalchemy.orm import scoped_session
from slots import MAB

# from .decorators import background, email, limit
from .utils import build_next_res, find_project_item_option, update_item
from ..database import Item, Option
from ..utils import hash_id

# TODO: handle POST case where item already exists (id)
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
    def get_next_item():
        """GET - get the next option in line for the given item."""

        # Extract token and id from request body
        token = request.args.get("token")
        item_id = request.args.get("item_id")

        # Find project by token and item by id
        query_data = find_project_item_option(token=token, item_id=item_id)
        if "error" in query_data:
            return query_data["error"]

        # Build a json response object
        return build_next_res(query_data)

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

    # ***********************
    #  PATCH --- UPDATE ITEM
    # ***********************
    # @email
    @items.route("/", methods=["PATCH"])
    # @background
    def next_trial() -> str:
        """PATCH - retrieve the next option in line, and update `next`, or end the trial."""

        # Extract token, item_id, option_num and clicked from request body
        token = request.form.get("token")
        item_id = request.form.get("item_id")
        option_num = int(request.form.get("option_num")) - 1  # bandit is 0 indexed
        clicked = 1 if request.form.get("clicked").capitalize() == "True" else 0

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
        return update_item(db_session, query_data, trial_results, mab)

    # **********************************
    #  PATCH --- INITIALIZE MAB ON ITEM
    # **********************************
    # @email
    @items.route("/init/", methods=["PATCH"])
    def initialize_mab() -> str:
        """Initialize the multi-armed bandit for an item, and update item's row with the MAB test class instance."""

        # Extract token and id from request body
        token = request.form.get("token")
        item_id = request.form.get("item_id")

        # Find project by token and item by id
        query_data = find_project_item_option(token=token, item_id=item_id)
        if "error" in query_data:
            return query_data["error"]

        # Check to see if the trial has already begun
        if query_data["item"].mab:
            return "This trial has already begun."

        # Check to see if at least two options are associated with item
        if query_data["item"].total_num < 2:
            return "There must be at least two options for each item to run a trial."

        # Create a new instance of th MAB test class, pickle it, and store it in the db
        pickled_mab = pickle.dumps(MAB(num_bandits=query_data["item"].total_num))
        query_data["item"].mab = pickled_mab
        query_data["item"].active_trial = True

        try:
            db_session.add(query_data["item"])
            db_session.commit()
        except:
            return "500 - internal server error."

        return "MAB successfully initiated, trials are ready to begin!\n\nYou can no longer add, or delete options. You must delete this item if you wish to make changes."

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
