#!/usr/bin/env python3
"""Unit tests for project model."""

import uuid


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ------------------------- * PROJECT TESTS * -----------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_fields_on_new_project(new_project) -> None:
    """
    GIVEN a Project model
    WHEN a new Project is created
    THEN check that the id, token, title, email, phone and verification fields are defined correctly
    """

    # assert isinstance(new_project.id, int)  # not created yet, hasnt been committed
    assert isinstance(new_project.token, uuid.UUID)
    assert new_project.title == "Lord of the Rings"
    assert new_project.email == "J. R. R. Tolkien"
    assert new_project.phone == "5558675309"
    assert new_project.verification is None
