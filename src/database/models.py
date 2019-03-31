#!/usr/bin/env python3
"""Contains models for Project, Item and Option"""

from uuid import uuid4

from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.hybrid import hybrid_property

from ._db import Base
from .guid import GUID
from ..utils import hash_id

# TODO: default value for item when no option, ensure this if options deleted

# can you associate based on virtual fields? s--- would i need to?


class Project(Base):
    __tablename__ = "Projects"

    id = Column(Integer, primary_key=True)
    token = Column(GUID, nullable=False, unique=True)
    title = Column(Text, nullable=False, unique=True)
    email = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    verification = Column(Text)

    def __init__(self, title: str, email: str, phone: str):
        self.token = uuid4()
        self.title = title
        self.email = email
        self.phone = phone
        self.verification = None  # store email code, sms + new field here

    def __repr__(self):
        return {
            "id": self.id,
            "token": self.token,
            "title": self.title,
            "email": self.email,
            "phone": self.phone,
            "verification": self.verification,
        }

    def __str__(self):
        return "Project Model"


class Item(Base):
    __tablename__ = "Items"

    id = Column(Text, primary_key=True)
    total_num = Column(Integer, nullable=False)
    next = Column(
        Text,
        default="https://user-images.githubusercontent.com/1825286/26859182-9d8c266c-4afb-11e7-8913-93d29b3f47e5.png",
        nullable=False,
    )

    @hybrid_property
    def project_id(self) -> str:
        """'Un-hash' item's id to access the project's id, and return the project's id."""
        return self.id.split(":")[0]

    def __init__(self, project_id: str, item_id: str or int):
        self.id = hash_id(project_id, item_id)
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


class Option(Base):
    __tablename__ = "Options"

    id = Column(Text, primary_key=True)
    content = Column(Text, nullable=False)

    @hybrid_property
    def project_id(self) -> str:
        """'Un-hash' option's id to access the project's id, and return the project's id."""
        return self.id.split(":")[0]  # project is first part of id hash

    @hybrid_property
    def item_id(self) -> str:
        """'Un-hash' option's id to access the item's id, and return the items's id."""
        return self.id.split(":")[1]  # item is second part of id hash

    def __init__(self, project_id: str, item_id: str, option_num: int, content: str):
        self.id = hash_id(project_id, item_id, option_num)
        self.content = content

    def __repr__(self):
        return {"id": self.id, "content": self.content}

    def __str__(self):
        return "Option Model"
