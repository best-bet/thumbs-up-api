#!/usr/bin/env python3
"""RESTful projects route, contains routes for GET, POST, PATCH, and DELETE."""

from envelopes import Envelope
from flask import Blueprint, render_template, request
from sqlalchemy.orm import scoped_session

# from .decorators import background, email, limit
from .utils import find_project_item_option
from ..database import Project, Item, Option
from ..utils import hash_id, Validate

# TODO: handle POST case where project already exists (title)
# TODO: implement email on project creation
# TODO: email verification to edit project
# TODO: require email verification to delete project
# TODO: error handle --- token invalid, etc.
# TODO: implement decorators


def projects_api_route(db_session: scoped_session) -> Blueprint:
    """Wrapper for projects Blueprint, passes db connection to routes."""

    # Blueprint for projects
    projects = Blueprint(
        "projects",
        __name__,
        template_folder="src.templates",
        url_prefix="/api/projects",
    )

    # *****************************
    #  GET --- GET PROJECT (title)
    # *****************************
    @projects.route("/", methods=["GET"])
    # @limit(requests=100, window=(24 * 60 * 60 * 1000), by="ip")  # limit: 100 requests per day by ip
    def get_project_title():
        """GET - get the title of the project given a project token."""

        # Extract token from query string
        token = request.args.get("token")

        # Retrieve project with token
        query_data = find_project_item_option(token=token)
        if "error" in query_data:
            return query_data["error"]

        return query_data["project"].title

    # *************************
    #  POST --- CREATE PROJECT
    # *************************
    @projects.route("/", methods=["POST"])
    # @limit(requests=100, window=(24 * 60 * 60 * 1000), by="ip")  # limit: 100 requests per day by ip
    # @email
    def create_project():
        """POST - create a project given a `title`, `email` and `phone`."""

        # Extract request body
        title = request.form.get("title")
        email = request.form.get("email")
        phone = request.form.get("phone")

        if not Validate.title(title):
            return 'Please provide valid title: alphanumeric characters, "-", "_", and "." are valid.'
        if not Validate.email(email):
            return "Please provide valid email."
        if not Validate.phone(phone):
            return "Please provide valid phone."

        try:
            # Create a new project from the query params
            new_project = Project(title=title, email=email, phone=phone)
            db_session.add(new_project)
            db_session.commit()
        except:
            db_session.rollback()
            return "500 - internal server error."

        # # when creating a new project, send confirmation email...
        # envelope = Envelope(
        #     to_addr=email,
        #     from_addr=(u'from@example.com', u'the team at thumbs up'),
        #     subject="Thank you for creating a new project with thumbs up!",
        #     text_body="this works?",  # render_template('src/templates/email.txt'),
        #     html_body=render_template('src/templates/email.html')
        # )
        #
        # # Send the envelope using an ad-hoc connection...
        # envelope.send('smtp.googlemail.com', login='kyleuehlein@gmail.com', password='notpassword', tls=True)

        return f"<h1>title={title}, email={email}, phone={phone}, token={new_project.token}</h1>"  # not this

    # **************************
    #  PATCH --- UPDATE PROJECT
    # **************************
    @projects.route("/", methods=["PATCH"])
    # @limit(requests=100, window=(24 * 60 * 60 * 1000), by="ip")  # limit: 100 requests per day by ip
    # @email
    def update_project():
        """PATCH - edit a project given the respective fields; `title`, `email`, `phone` or `token`."""

        # Extract request body
        title = request.form.get("title")
        email = request.form.get("email")
        phone = request.form.get("phone")
        token = request.form.get("token")

        # Retrieve project with token
        query_data = find_project_item_option(token=token)
        if "error" in query_data:
            return query_data["error"]

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

    # ***************************
    #  DELETE --- DELETE PROJECT
    # ***************************
    @projects.route("/", methods=["DELETE"])
    # @limit(requests=100, window=(24 * 60 * 60 * 1000), by="ip")  # limit: 100 requests per day by ip
    # @email
    def delete_project() -> str:
        """DELETE - delete a project and all associated data given a `token`."""

        # Extract token from query string
        token = request.form.get("token")

        # Retrieve project with token
        query_data = find_project_item_option(token=token)
        if "error" in query_data:
            return query_data["error"]

        # Retrieve all items associated with the project
        project_items = Item.query.filter_by(project_id=query_data["project"].id)

        print("\n\n\n\nproject_items", project_items, "\n\n\n\n")

        # Iterate through all of the items and options related to the project and delete them
        for item in project_items:
            for i in range(1, item.count + 1):
                option = Option.query(hash_id(query_data["project"].id, item.id, i))
                db_session.delete(option)

            db_session.delete(item)

        try:
            db_session.delete(query_data["project"])
            db_session.commit()
        except:
            db_session.rollback()
            return "500 - internal server error."

        return f"{query_data['project'].title} and all related data was successfully deleted."

    # Return projects Blueprint
    return projects
