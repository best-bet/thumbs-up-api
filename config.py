#!/usr/bin/env python3
"""Flask configs for Production, Staging, Development and Testing"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data.sqlite")
    DEBUG = False
    SECRET_KEY = "The Gracehoper was always jigging ajog, hoppy on akkant of his joyicity, (he had a partner pair of findlestilts to supplant him)"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "mysql://kyleuehlein@localhost/thumbs-up-api"
    )
    DEBUG = False


class StagingConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.data.sqlite")
    TESTING = True
    WTF_CSRF_ENABLED = False
