#!/usr/bin/env python3
"""
options route
"""

from server import app  # coming from server
from db._db import db  # coming from server
from db.models.item import Item  # coming from server
from db.models.option import Option  # coming from server
from ..utils import hash_id


# /api/projects/<project_id>/items/<item_id>/options

# *GET* - get an option
@app.route("/<option_num>")
def get_option(option_num: str):
    """
    id from project + id from item + option number = option id
    """
    hashed_option_id = hash_id(project_id, item_id, option_num)

    return Option.query.get(
        hashed_option_id
    )  # not sure what to return --- use with MAB


# *POST* - create new option
@app.route("/<option_num>/<option_data>")
def create_option(option_num: str, option_data: str):
    """
    create a new option with `id` and `item`
    data for MAB is also here

    `option_data` should look like this: item_id=1234-5678-1234-5678:8888-8888-8888&url=https://mysite.com/assets/mypic.jpg&item_count=1

    id from project + id from item + option number = option id

    a new option associated with a item should be created
    """

    content = option_data  # format this

    new_option = Option(project_id, item_id, option_num, content)
    db.session.add(new_option)
    db.session.commit()

    return new_option  # what to return ???


# *PATCH* - update option with new MAB data
@app.route("/<option_num>")
def update_option(option_num: str) -> None:
    """
    update MAB data if item was clicked
    """

    hashed_option_id = hash_id(project_id, item_id, option_num)

    option = Option.query(hashed_option_id)
    Option.add(option)
    Option.commit()

    # return might not be necessary


# *DELETE* - delete an option
@app.route("/<content_to_delete>")
def delete_option(content_to_delete: str) -> str:
    """
    Delete an option for an item given an input `content_to_delete`.
    """

    hashed_item_id = hash_id(project_id, item_id)
    item = Item.query(hashed_item_id)

    # check each option for a match with content to delete
    for i in range(1, item.total_num + 1):
        option_id = hash_id(project_id, item_id, i)
        option = Option.query(option_id)
        if option.content == content_to_delete:
            # delete right away if this is the last item
            if i == item.total_num:
                db.session.delete(option)
            # swap item with last item, and delete new last item
            else:
                last_option_id = hash_id(project_id, item_id, item.total_num)
                last_option = Option.query(last_option_id)
                last_option.id = option.id
                db.session.add(last_option)
                db.session.delete(option)
            break

    item.count -= 1
    db.Session.add(item.count)

    if item.next == content_to_delete:
        # do some MAB magic and find the next value
        pass

    db.Session.commit()

    return "deletion successful"
