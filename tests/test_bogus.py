"""Bogus tests to test the test system."""

import pytest


def test_bogus():
    """Test whether one is one."""
    assert 1 == 1


def test_raises():
    """Test a simple raising function."""

    def raises():
        raise Exception("This raises!")

    with pytest.raises(Exception, match="This raises!"):
        raises()
