"""Json schemas validator."""
# -*- coding: utf-8 -*-

from json import dumps
from datetime import datetime
from json_validator.validator import JsonValidator


def test_validator_needs_constrain():
    """Test validator needs constrain."""
    try:
        JsonValidator('')
        assert False
    except AttributeError:
        pass

    assert JsonValidator({})


def test_validator_valid_json():
    """Test validator recieves a valid json."""
    res, err = JsonValidator._convert("{'foo': 'bar'}")
    assert err == '1' and not res

    data = {'foo': 'bar'}
    res, err = JsonValidator._convert(dumps(data))
    assert res == data and not err

    res, err = JsonValidator._convert(1.0)
    assert err and not res


def test_recieves_invalid_payload():
    """Test invalid payload retrival."""
    res, err = JsonValidator({}).validate('{as: "df"}')
    assert res is None and err == {'payload': 'INVALID PAYLOAD'}


def test_constrain_primitive():
    """Test constrain primitive types."""
    constrain = {
        'string': {},
        'integer': {'type': int},
        'float': {'type': float},
        'boolean': {'type': bool},
        'json': {
            'type': dict
        },
        'list': {
            'type': list,
        },
    }
    json = {
        'string': 'foo',
        'integer': 42,
        'float': 1.10,
        'boolean': True,
        'json': {},
        'list': []
    }
    json2 = json.copy()
    JsonValidator.clean_data(json2)
    res, err = JsonValidator(constrain).validate(json)
    assert res == json2 and not err


def test_invalid_type():
    """Test invalid types."""
    constrain = {
        'string': {},
        'extra_1': {},
        'extra_2': {},
    }
    json = {
        'string': 1234
    }

    res, err = JsonValidator(constrain).validate(json)
    assert err == {'string': 'Bad data type',
                   'extra_1': 'Missing field', 'extra_2': 'Missing field'}


def test_constrain_lists_dicts():
    """Test nested structures."""
    constrain = {
        'json': {
            'type': dict,
            'properties': {
                'integer': {'type': int},
                'float': {'type': float},
            }
        },
        'list': {
            'type': list,
            'items': {
                'type': dict,
                'properties': {
                    'name': {},
                    'lastname': {},
                    'age': {
                        'type': list,
                        'items': {
                            'type': int
                        }
                    }
                }
            }
        },
    }
    json = dumps({
        'json': {
            'integer': 42,
            'float': 12.12
        },
        'list': [{
            'name': 'johan',
            'lastname': 'mogollon',
        }, {
            'name': 'johan',
            'lastname': 'mogollon',
        }, {
            'name': 'jean',
            'lastname': 'paul',
            'age': [12, 24]
        }]
    })

    res, err = JsonValidator(constrain).validate(json)
    assert res == {
        'json': {'float': 12.12, 'integer': 42},
        'list': [
            {'lastname': 'mogollon', 'name': 'johan'},
            {'lastname': 'mogollon', 'name': 'johan'},
            {'age': [12, 24], 'lastname': 'paul', 'name': 'jean'}
        ]}
    assert err == {
        'list': [
            {'list.0.age': 'Missing field'},
            {'list.1.age': 'Missing field'}
        ]
    }

    json = dumps({
        'json': {
            'integer': 42,
            'float': 12.12
        },
        'list': [42, 61, 22]
    })

    res, err = JsonValidator(constrain).validate(json)
    assert res == {'json': {'float': 12.12, 'integer': 42}}
    assert err == {'list': ['Bad data type', 'Bad data type', 'Bad data type']}


def test_number_rules():
    """Test rules on fields which are numbers."""
    constrain = {
        'integer': {
            'type': int,
            'gt': -1,
            'lt': 101
        },
        'float': {
            'type': float,
            'gt': -1,
            'lt': 101
        }
    }
    json = {'integer': 101, 'float': -1.0}
    res, err = JsonValidator(constrain).validate(json)
    assert not res and err == {'integer': 'Not less than 101',
                               'float': 'Not greater than -1'}

    json = {'integer': -1, 'float': 101.0}
    res, err = JsonValidator(constrain).validate(json)
    assert not res and err == {'integer': 'Not greater than -1',
                               'float': 'Not less than 101'}


def test_regex_rule():
    """Test fields ruled by regex."""
    constrain = {
        'number': {
            'format': r'^\d+$',
        }
    }
    json = {'number': 'one hundred'}
    res, err = JsonValidator(constrain).validate(json)
    assert err == {'number': 'Invalid format'} and not res

    json = {'number': '42'}
    res, err = JsonValidator(constrain).validate(json)
    assert res == json and not err


def test_default_rule():
    """Test fields ruled by regex."""
    constrain = {
        'number': {
            'format': r'^\d+$',
            'default': 42
        }
    }
    json = {}
    res, err = JsonValidator(constrain).validate(json)
    assert res == {'number': 42} and not err


def test_inclusion_rule():
    """Test fields ruled by inclusion in list."""
    constrain = {
        'fruit': {
            'in': ['apple', 'orange', 'pineapple']
        }
    }
    json = {'fruit': 'cherry'}
    res, err = JsonValidator(constrain).validate(json)
    assert not res and err == {'fruit': 'Invalid'}

    json = {'fruit': 'apple'}
    res, err = JsonValidator(constrain).validate(json)
    assert res == {'fruit': 'apple'} and not err


def test_datetime_rule():
    """Test fields is a datetime with custom format."""
    constrain = {
        'birthdate': {
            'type': datetime,
        }
    }
    json = {'birthdate': '1990-12-24'}

    try:
        JsonValidator(constrain).validate(json)
        assert False
    except AttributeError:
        assert True

    constrain['birthdate']['dformat'] = '%Y-%m-%d'
    res, err = JsonValidator(constrain).validate(json)
    assert not err and res == {
        'birthdate': datetime.strptime('1990-12-24', '%Y-%m-%d')}

    json = {'birthdate': '1990-13-24'}
    res, err = JsonValidator(constrain).validate(json)
    assert not res and err == {'birthdate': 'Invalid format'}


def test_lazy_validation():
    """Test validation exit when first error found."""
    constrain = {
        'a': {'type': int, 'gt': 10},
        'b': {'type': int, 'lt': 100}
    }
    json = {'a': 'a', 'b': 'b'}  # lazy case diferent type
    res, err = JsonValidator(constrain, lazy=True).validate(json)
    assert not res and len(err) == 1

    json = {'a': 9, 'b': 101}  # lazy extra validation
    res, err = JsonValidator(constrain, lazy=True).validate(json)
    assert not res and len(err) == 1

    constrain = {
        'birthdate': {'type': datetime, 'dformat': '%Y'},
        'birthdate2': {'type': datetime, 'dformat': '%Y'}
    }
    json = {  # lazy special type
        'birthdate': '1990-12-24',
        'birthdate2': '1990-12-24'
    }
    res, err = JsonValidator(constrain, lazy=True).validate(json)
    assert not res and len(err) == 1

    json = {}  #  empty field lazy error
    res, err = JsonValidator(constrain, lazy=True).validate(json)
    assert not res and len(err) == 1

    constrain = {  # lazy dict field
        'a': {
            'type': dict,
            'properties': {'b': {}}
        },
        'c': {
            'type': dict,
            'properties': {'d': {}}
        },
    }
    json = {'a': {}, 'b': {}}
    res, err = JsonValidator(constrain, lazy=True).validate(json)
    assert len(err) == 1

    constrain = {  # lazy list field
        'a': {
            'type': list,
            'items': {'type': int}
        },
        'b': {
            'type': list,
            'items': {'type': int}
        },
    }
    json = {'a': ['a'], 'b': ['b']}
    res, err = JsonValidator(constrain, lazy=True).validate(json)
    assert len(err) == 1


def test_error_messages():
    """Test validation exit when first error found."""
    constrain = {
        'a': {
            'type': int,
            'type_error': 'my message'
        },

        'b': {
            'type': int,
            'gt': 10,
            'gt_error': '{value} not gt than {limit} error'
        },

        'c': {
            'type': int,
            'gt': 20,
            'gt_error': 'Not gt than {limit} error'
        },

        'd': {
            'format': r'^\d+$',
            'format_error': 'Invalid format regex'
        },

        'e': {
            'in': ['potato'],
            'in_error': 'Not allowed'
        },

        'f': {
            'type': datetime,
            'dformat': '%Y-%m-%d',
            'dformat_error': 'Invalid date format'
        },

        'g': {
            'error': 'Not retrieved'
        }
    }
    json = {
        'a': {}, 'b': 10, 'c': 20, 'd': 'foo', 'e': 'bar', 'f': '18-08-2017'}
    res, err = JsonValidator(constrain).validate(json)
    assert not res and err == {
        'a': 'my message',

        'b': constrain['b']['gt_error'].format(
            value=json.get('b', ''), limit=constrain['b']['gt']),

        'c': constrain['c']['gt_error'].format(limit=constrain['c']['gt']),

        'd': 'Invalid format regex',

        'e': 'Not allowed',

        'f': 'Invalid date format',

        'g': 'Not retrieved',

    }


def test_invalid_payload_error_message():
    """Set message for invalid payload or constrain."""
    decode_error = {'payload': 'Error on payload submitted'}
    res, err = JsonValidator(
        {}, decode_error=decode_error).validate('{as: "df"}')
    assert res is None and err == decode_error

    data_error = {'data': 'Error on constrain submitted'}
    res, err = JsonValidator({}, decode_error=data_error).validate(42)
    assert res is None and err == data_error


def test_calls_default_lambda():
    """Test default lambda is called when obtaining default."""
    constrain = {
        'expiration': {
            'type': datetime,
            'default': lambda: datetime.now()
        }
    }
    json = {}
    comparative = datetime.now()
    res, err = JsonValidator(constrain).validate(json)
    assert res and not err

    assert res['expiration'] > comparative
