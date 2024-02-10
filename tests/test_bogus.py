import pytest


def test_bogus():
    assert 1 == 1


def test_raises():
    def raises():
        raise Exception("This raises!")

    with pytest.raises(Exception, match="This raises!"):
        raises()
