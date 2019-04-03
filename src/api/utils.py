#!/usr/bin/env python3
"""Utility functions, includes: `find_project_item_option`."""

import pickle

from slots import MAB
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from ..database import Project, Item, Option
from ..utils import hash_id

# TODO: find SQLAlchemy error types to distinguish between SQLAlchemy error and incorrect user input


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
        except NoResultFound as err:
            data["error"] = err
        except:
            data["error"] = "Token invalid."  # sys.exc_info()[0]
            return data
    else:
        data["error"] = "500 - internal server error: invalid input."
        return data

    # If item_id is provided, find item and handle errors, else return `data`
    if "item_id" in kwargs:
        try:
            data["item"] = Item.query.get(hash_id(data["project"].id, kwargs["item_id"]))
        except NoResultFound as err:
            data["error"] = err
        except:
            data["error"] = "Item id invalid."
            return data
    else:
        return data

    # If option_num is provided, find option and handle errors, else return `data`
    if "option_num" in kwargs:
        try:
            data["option"] = Option.query.get(hash_id(data["project"].id, kwargs["item_id"], kwargs["option_num"]))
        except NoResultFound as err:
            data["error"] = err
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

    # Create a list to hold values that need to be updated, and add the pickled mab to it
    update = [pickle.dumps(mab)]

    # Update the information
    if trial_results["new_trial"]:
        if trial_results["choice"] != query_data["item"].next:
            query_data["item"].next = trial_results["choice"]
            update.append(query_data["item"])

        if trial_results["best"] != query_data["item"].best:
            query_data["item"].best = trial_results["best"]

            if query_data["item"] not in update:
                update.append(query_data["item"])

    # The trial is over, set `next` to the best preforming thumbnail and `active_trial` to False
    else:
        query_data["item"].next = trial_results["best"]
        query_data["item"].best = trial_results["best"]
        query_data["item"].active_trial = False

        # Delete all options as they are no longer needed
        for i in range(1, query_data["item"].total_num + 1):
            option_id = hash_id(query_data["project"].id, query_data["item"].id, i)
            Option.query.filter_by(id=option_id).delete()

        query_data["item"].total_num = 0
        update.append(query_data["item"])

    try:
        db_session.add_all(update)
        db_session.commit()
        return "200 - trial successfully updated."
    except:
        return "500 - internal server error."
