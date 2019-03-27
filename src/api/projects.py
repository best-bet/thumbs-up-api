#!/usr/bin/env python3
"""project route"""

from src import app  # this will be passed by server

from database import db, Project, Item, Option  # this will be from app
from ..utils import hash_id

# /api/projects


# *GET* - get a project
@app.route("/<id>", methods=["GET"])
def get_project(id: str):  # uuid4()?
    """
    user can request any info on the project except `sms` and `verification_code`
    can search by:
        *id -------- might not need this (user has token, not id)
        *title
        *token
    """

    # ? user has to specify what they want back? `return_val=email` - grab email field

    return Project.query.get(id).title  # not sure what to return


# *POST* - create new project
@app.route("/<new_project_data>", methods=["POST"])  # how to say post req?
def create_project(new_project_data: str) -> int:
    """
    create a new project with `title`, `email`, `phone`
    `sms, and `verification_code` are also fields here

    `new_project_data` should look like this: title=my-title&email=my.email@email.com&phone=1234567890

    send email with new project id

    if email is not sent, sent to wrong place, HOW TO DELETE?
    """

    title, email, phone = new_project_data  # format this

    new_project = Project(title, email, phone)
    db.session.add(new_project)
    db.session.commit()

    # email???

    return new_project  # not sure what to returns


# *PATCH* - edit project
@app.route("/<token>/<new_data>", methods=["PATCH"])
def edit_project(token: str):
    """
    which fields are editable / verification necessary?

    title=my-new-title
    email=mynewemail@email.com
    phone=9999999999
    token --- new uuid
    sms=123456
    verification=123456
    """

    project = Project.query.filter_by(token=token)

    # only change one thing at a time
    # if change email, send sms to phone and verification to new email
    # if change phone, send sms to new phone and verification to email
    # if change title or token, send sms to phone and verification to email

    # if user submits sms and verification that match what is in db
    # set both to null and update with provided email

    # ! where to store new value that is being changed before verification?
    # * mush it into the sms + verification code field?
    # * should i even have sms and verification fields? --- this is a lot of space
    # * for an operation that hardly ever happens

    return "changed"  # not sure what to return


# *DELETE* - delete project
@app.route("/<token>", methods=["DELETE"])
def delete_project(token: str):
    """
    delete project, all associated item and all of their associated options

    should there be an email verification?

    how will items with the id be found?
        - ids like this one? (match project_id at front of item_id)
        - then delete options assoc.
    """
    project = Project.query.filter_by(token=token)
    project_items = Item.query.filter_by(title=project.title)

    for item in project_items:
        for i in range(1, item.count + 1):
            option = Option.query(hash_id(project_id, item_id, i))
            db.session.delete(option)
        db.session.delete(item)

    db.session.delete(project)
    db.session.commit()

    return "project deleted"  # not sure what to return
