#!/usr/bin/env python3
"""item route"""

from server import app  # will be from server
from database._db import db # will be from server
from database.models import Project, Item, Option # will be from server
from ..utils import hash_id


# /api/projects/<project_id>/items

# *GET* - get an item
@app.route("/<item_id>")
def get_catagory(item_id: str):
    """
    get next item, then find the following item
    """
    hashed_item_id = hash_id(project_id, item_id)
    next_item = Item.query.get(hashed_item_id).next

    # calculate next item using MAB + set next item to item.next
    # ! can i calculate after sending response?

    return next_item


# *POST* - create new item
@app.route("/<item_id>")
def create_item(item_id: str):
    """
    create new id by hashing project_id and id provided, then create a new item

    if MAB cant add new items after starting, bulk create options at same time

    USER MUST USE A UNIQUE IDENTIFIER (include this in the docs)


    """

    # ! how to grab project id from further down the route?

    project_title = Project.query(project_id).title

    # sanitize item_id to protect against sql injection

    new_item = Item(project_id, item_id, project_title)
    db.session.add(new_item)
    db.session.commit()

    # * if MAB wont let me add more options after starting, do this:
    # db.session.add_all(arr_of_options)
    # db.session.commit()

    return new_item


# *PATCH* - add update if item was clicked
def update_item(item_id: str) -> None:
    """
    if image was clicked, factor that into MAB, update item.next if necessary
    """
    # ! update data for MAB, calculate `item.next`
    # no return necessary


# *DELETE* - delete an item
@app.route("/create/<item_id>")
def delete_item(item_id: str):
    """
    Delete item with given id and all of the options associated with it
    """

    # how to grab project id from further down the route?
    hashed_item_id = hash_id(project_id, item_id)
    item = Item.query(hashed_item_id)

    for i in range(1, item.count + 1):
        option = Option.query(hash_id(project_id, item_id, i))
        db.session.delete(option)

    db.session.delete(item)
    db.session.commit()

    return "deleted"  # what is returned?
