#!/usr/bin/env python3
"""Contains models for Project, Item and Option"""

from uuid import uuid4

from sqlalchemy import Column, Integer, Text

from ._db import Base
from .guid import GUID
from ..utils import hash_id

# TODO: better way to store sms/verif-code + new email/phone/etc. ?
# TODO: default value for item when no option, ensure this if options deleted

# TODO: how to pass `db.Model`???


class Project(Base):
    __tablename__ = "Projects"

    id = Column(Integer, primary_key=True)
    token = Column(GUID, nullable=False)
    title = Column(Text, nullable=False, unique=True)
    email = Column(Text, nullable=False)
    phone = Column(Text, nullable=False)
    sms = Column(Text)
    verification_code = Column(Text)

    def __init__(self, title: str, email: str, phone: str):
        self.token = uuid4()
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
        return f"Project Model --- email: {self.email}, title: {self.title}"


class Item(Base):
    __tablename__ = "Items"

    id = Column(Text, primary_key=True)
    project_title = Column(Text, nullable=False)
    total_num = Column(Integer, nullable=False)
    next = Column(
        Text,
        default="https://user-images.githubusercontent.com/1825286/26859182-9d8c266c-4afb-11e7-8913-93d29b3f47e5.png",
        nullable=False
    )

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


class Option(Base):
    __tablename__ = "Options"

    id = Column(Text, primary_key=True)
    content = Column(Text, nullable=False)  # ! better data type for url?

    def __init__(self, project_id: str, item_id: str, option_num: str, content: str):
        self.id = hash_id(project_id, item_id, option_num)
        self.content = content

    def __repr__(self):
        return {"id": self.id, "content": self.content}

    def __str__(self):
        return "Option Model"
