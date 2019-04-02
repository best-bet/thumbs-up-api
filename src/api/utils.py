#!/usr/bin/env python3
"""Utility functions, includes: `find_project_item_option`."""

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
