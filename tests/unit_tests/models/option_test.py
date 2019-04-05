#!/usr/bin/env python3
"""Unit tests for option model."""


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  -------------------------- * OPTION TESTS * -----------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_fields_on_new_option(new_project, new_item, test_option):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """

    # assert test_option.id == new_project.id + ":" + new_item.id + ":" + "1"
    assert test_option.content == "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Walrus_(Odobenus_rosmarus)_on_Svalbard.jpg/1920px-Walrus_(Odobenus_rosmarus)_on_Svalbard.jpg"
