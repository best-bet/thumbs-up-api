#!/usr/bin/env python3
"""Contains models for Project, Item and Option"""

from uuid import uuid4

from sqlalchemy import Boolean, Column, Integer, PickleType, Text

from ._db import Base
from .guid import GUID
from ..utils import hash_id


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

    def __repr__(self):
        return f"id: {self.id}, token: {self.token}, title: {self.title}, email: {self.email}, phone: {self.phone}"

    def __str__(self):
        return "Project Model"


class Item(Base):
    __tablename__ = "Items"

    id = Column(Text, primary_key=True)
    total_num = Column(Integer, default=0,  nullable=False)
    active_trial = Column(Boolean, default=False, nullable=False)
    mab = Column(PickleType)
    next = Column(Text)
    option_num = Column(Integer)

    def __init__(self, project_id: str, item_id: str or int):
        self.id = hash_id(project_id, item_id)

    def __repr__(self):
        return f"id: {self.id}, total_num: {self.total_num}, next: {self.next}"

    def __str__(self):
        return "Item Model"


class Option(Base):
    __tablename__ = "Options"

    id = Column(Text, primary_key=True)
    content = Column(Text, nullable=False)

    def __init__(self, project_id: str, item_id: str, option_num: int, content: str):
        self.id = hash_id(project_id, item_id, option_num)
        self.content = content

    def __repr__(self):
        return f"id: {self.id}, content: {self.content}"

    def __str__(self):
        return "Option Model"
