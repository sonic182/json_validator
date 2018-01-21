
import pytest


@pytest.fixture
def validator():
    """Return validator fixture."""
    from json_validator import JsonValidator
    return JsonValidator


@pytest.fixture
def dumps():
    """Return json dumps fixture."""
    from json import dumps
    return dumps

