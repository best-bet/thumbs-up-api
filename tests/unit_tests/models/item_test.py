#!/usr/bin/env python3
"""Unit tests for item model."""


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  --------------------------- * ITEM TESTS * ------------------------
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def test_fields_on_new_item(new_project, new_item):
    """
    GIVEN an Item model
    WHEN a new Item is created
    THEN check that the id, total_num, active_trial, mab, next, and option_num fields are defined correctly
    """

    # assert new_item.id == new_project + ":" + "1"
    # assert new_item.total_num == 0
    # assert new_item.active_trial is False
    assert new_item.mab is None
    assert new_item.next is None
    assert new_item.option_num is None
