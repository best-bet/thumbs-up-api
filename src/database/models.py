#!/usr/bin/env python3
"""Contains models for Project, Item and Option"""

from flask_sqlalchemy import SQLAlchemy

from .guid import GUID
from ..utils import hash_id

# TODO: figure out associations, and do i need them?
# TODO: better way to store sms/verif-code + new email/phone/etc. ?
# TODO: default value for item when no option, ensure this if options deleted

# TODO: FIRST --- GUID causes error during migration.


def register_models(db: SQLAlchemy):
    """Register models by passing down a db connection. Returns a dictionary containing all models."""

    class Project(db.Model):
        __tablename__ = "Projects"

        id = db.Column(db.Integer, primary_key=True)
        token = db.Column(GUID, nullable=False)  # <----- not happy about GUID
        title = db.Column(db.Text, nullable=False, unique=True)
        email = db.Column(db.Text, nullable=False)
        phone = db.Column(db.Text, nullable=False)
        sms = db.Column(db.Text)
        verification_code = db.Column(db.Text)

        # # one Project, many Items
        # items = db.relationship("Item", backref="Project", lazy="subquery", uselist=False)

        def __init__(self, title: str, email: str, phone: str):
            # self.token = uuid.uuid4()
            self.title = title
            self.email = email
            self.phone = phone
            self.sms = None
            self.verification_code = None

        def __repr__(self):
            return {
                "id": self.id,
                # 'token': self.token,
                "title": self.title,
                "email": self.email,
                "phone": self.phone
                # 'sms': self.sms,
                # 'verification_code': self.verification_code
            }

        def __str__(self):
            return "Project Model"

    class Item(db.Model):
        __tablename__ = "Items"

        id = db.Column(db.Text, primary_key=True)
        project_title = db.Column(db.Text, nullable=False)
        total_num = db.Column(db.Integer, nullable=False)
        next = db.Column(
            db.Text,
            default="https://user-images.githubusercontent.com/1825286/26859182-9d8c266c-4afb-11e7-8913-93d29b3f47e5.png",
            nullable=False
        )

        # # one Item, One Project
        # project = db.relationship("Project", backref="Item", uselist=False)
        # # one Item, many Options
        # options = db.relationship("Item", backref="Item", lazy="subquery", uselist=False)

        def __init__(self, project_id: str, item_id: str, project_title: str):
            self.id = hash_id(project_id, item_id)
            self.project_title = project_title
            self.total_num = 0
            # any other data needed for MAB might go here

        def __repr__(self):
            return {
                "id": self.id,
                "project_title": self.project_title,
                "total_num": self.total_num,
                "next": self.next,
            }

        def __str__(self):
            return "Item Model"

    class Option(db.Model):
        __tablename__ = "Options"

        id = db.Column(db.Text, primary_key=True)
        content = db.Column(db.Text, nullable=False)  # ! better data type for url?

        # # one Option, One Item
        # item = db.relationship("Item", backref="Option", uselist=False)

        def __init__(self, project_id: str, item_id: str, option_num: str, content: str):
            self.id = hash_id(project_id, item_id, option_num)
            self.content = content

        def __repr__(self):
            return {"id": self.id, "content": self.content}

        def __str__(self):
            return "Option Model"

    # return a dictionary containing all models
    return {"Project": Project, "Item": Item, "Option": Option}
