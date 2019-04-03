#!/usr/bin/env python3
"""Utility functions, includes: `find_project_item_option`."""

import json
import pickle
import random

from slots import MAB
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from ..database import Project, Item, Option
from ..utils import hash_id

# TODO: item.option_num is being retrieved as `bytes`, currently converting to int, but find out what is happening???
# TODO: find SQLAlchemy error types to distinguish between SQLAlchemy error and incorrect user input
# TODO: deleting options after trial breaks RESTful convention, make a cleanup endpoint?


# Because of how the values are hashed for lookup convenience,
# it is very common to chain lookups together. This function
# DRYs lookup and error-handling for this very common operation.
def find_project_item_option(**kwargs: str or int) -> dict:
    """
    Given any number of the following keys, `token`, `item_id` and `option_num` kwargs,
    find all and return a dict containing this data.

    `"error"` property is added if there was an error during execution
    """

    # Dictionary containing response data and possibly an error message
    data = {}

    # If token is provided, find project by token and handle errors, else return "server error"
    if "token" in kwargs:
        try:
            data["project"] = Project.query.filter_by(token=kwargs["token"]).one()
        except NoResultFound:
            data["error"] = "Token invalid."
            return data
        except:
            data["error"] = "Token invalid."
            return data
    else:
        data["error"] = "500 - internal server error: invalid input."
        return data

    # If item_id is provided, find item and handle errors, else return `data`
    if "item_id" in kwargs:
        try:
            data["item"] = Item.query.get(hash_id(data["project"].id, kwargs["item_id"]))
        except NoResultFound:
            data["error"] = "Item id invalid."
            return data
        except:
            data["error"] = "Item id invalid."
            return data
    else:
        return data

    # If option_num is provided, find option and handle errors, else return `data`
    if "option_num" in kwargs:
        try:
            # item.id is already hashed, just add option_num
            data["option"] = Option.query.get(hash_id(data["item"].id, kwargs["option_num"]))
        except NoResultFound:
            data["error"] = "Option num invalid."
            return data
        except:
            data["error"] = "Option num invalid."
            return data

    return data


def update_item(db_session: scoped_session, query_data: dict, trial_results: dict, mab: MAB) -> None or str:
    """
    Check results of MAB trial against data in db, update db with trial results if necessary,
    as well as the pickled mab.

    If the trial has ended, set the best preforming thumbnail to be `next`, set `active_trial`
    to False, and delete all options associated with the item.
    """

    # Re-pickle mab class test instance
    query_data["item"].mab = pickle.dumps(mab)

    # If there are more trials, set the next url
    if trial_results["new_trial"]:
        if trial_results["choice"] != query_data["item"].next:
            # item.id is already hashed with project, just need to add option_num
            next_id = hash_id(query_data["item"].id, trial_results["choice"])
            query_data["item"].option_num = trial_results["choice"]

            # Find the next image using the id we get from `trial_results`
            try:
                option = Option.query.get(next_id)
                query_data["item"].next = option.content
            except:
                return "500 - internal server error"

    # The trial is over, set `next` to the best preforming thumbnail and `active_trial` to False
    else:
        query_data["item"].next = trial_results["best"]
        query_data["item"].active_trial = False

        # Delete all options as they are no longer needed
        for i in range(1, query_data["item"].total_num + 1):
            # item.id is already hashed, just add option_num
            option_id = hash_id(query_data["item"].id, i)
            Option.query.filter_by(id=option_id).delete()

        query_data["item"].total_num = 0

    try:
        db_session.add(query_data["item"])
        db_session.commit()
        return "200 - trial successfully updated."
    except:
        return "500 - internal server error."


def build_next_res(query_data: dict) -> json:
    """Construct a json object response that helps record the trial's results."""

    # Default information to be added to json response
    option_num = query_data["item"].option_num
    content = query_data["item"].next

    # If this is our first trial, select a random option to start
    if not query_data["item"].next:
        option_num = random.randint(1, query_data["item"].total_num)
        try:
            # item.id is already hashed with project, just need to add option_num
            option_id = hash_id(query_data["item"].id, option_num)
            option = Option.query.get(option_id)
            content = option.content
        except:
            return "500 - internal server error."

    return json.dumps({
        "url": content,
        "option_num": int.from_bytes(option_num, byteorder="little"),  # TODO: bytes??
        "send_data": query_data["item"].active_trial
    })
