"""Test imports errors"""


def test_import_error(mocker):
    import imp
    """Test import json.decoder error.

    This error happens with python versions 3.3 and 3.4
    """
    mocker.patch.dict('sys.modules', {'json.decoder': None})
    import json_validator
    imp.reload(json_validator)
