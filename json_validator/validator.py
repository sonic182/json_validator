"""Json schema validator module."""
# -*- coding: utf-8 -*-

from re import match
from datetime import datetime

from json import loads

try:
    from json.decoder import JSONDecodeError
    unicode = str
except ImportError:
    JSONDecodeError = ValueError

ERRORS = {
    '1': 'INVALID PAYLOAD',
    '2': 'INVALID DATA TYPE'
}


class JsonValidator:
    """Json Schema validator."""

    def __init__(self, constrain, lazy=False):
        """Set the constrain in object."""
        if not isinstance(constrain, dict):
            raise AttributeError('constrain must be a dict')
        self.constrain = constrain
        self.lazy = lazy

    def validate(self, data, field='', constrain=None, started=False):
        """Validate incoming data."""
        res = {}
        errors = {}
        err = None

        if not started:
            constrain = self.constrain
            data, err = self._convert(data)
            started = True

            if err:
                return (None, {'payload': ERRORS[err]})

        if constrain is None:
            return res, errors

        my_field = field
        for key in constrain:
            field = my_field
            field += '.' if my_field else ''
            field += key

            if key not in data:
                if constrain[key].get('default', False):
                    res[key] = constrain[key]['default']
                else:
                    errors[field] = 'Missing field'
                    if self.lazy:
                        break
            else:
                self._key_match(data[key], constrain[key], key, field, started,
                                res, errors)
                if errors and self.lazy:
                    return res, errors

        return res, errors

    def _key_match(self, obj, rules, key, field, started, res, errors):
        """Validate object with rueles."""
        if not isinstance(obj, (rules.get('type', str),
                                rules.get('type', unicode))):
            if self.special_types(obj, rules, key, field, res, errors):
                if errors and self.lazy:
                    return res, errors
            else:
                errors[field] = 'Bad data type'
                if self.lazy:
                    return res, errors

        elif self._extra_validations(obj, rules, errors, field):
            if self.lazy:
                return res, errors

        elif isinstance(obj, dict):
            res2, errors2 = self.validate(
                obj, field, rules.get('properties', None), started)

            res[key] = res2 or {}

            if errors2:
                errors[key] = errors2
                if self.lazy:
                    return res, errors

        elif isinstance(obj, list):
            res[key] = []
            my_field2 = field
            for ind, item in enumerate(obj):
                field = my_field2
                field += '.{}'.format(ind)
                res[key].append(None)

                res2, errors2 = self._key_match(item, rules.get(
                    'items', {}), ind, field, started, res[key], {})

                if res2:
                    res[key] = res2
                # Empty none items, required for recursivity to work
                res[key] = [x for x in res[key] if x is not None]

                if errors2:
                    if errors.get(key, None) is None:
                        errors[key] = []
                    errors[key].append(
                        errors2.get(ind, '') or errors2.get(field, ''))
                    if self.lazy:
                        return res, errors

        else:
            res[key] = obj

        return res, errors

    @staticmethod
    def special_types(obj, rules, key, field, res, errors):
        """Validate if special type retrieved."""
        if rules['type'] == datetime:
            if rules.get('dformat', False):
                try:
                    res[key] = datetime.strptime(obj, rules['dformat'])
                except ValueError:
                    errors[field] = 'Invalid format'
            else:
                raise AttributeError('Missing `dformat` on datetime rule')
            return True
        return False

    @staticmethod
    def _extra_validations(data, rules, errors, field):
        """Extras validations."""
        if isinstance(data, (int, float)):
            if rules.get('gt', False) and not data > rules['gt']:
                errors[field] = 'Not greater than %i' % rules['gt']
                return True

            elif rules.get('lt', False) and not data < rules['lt']:
                errors[field] = 'Not less than %i' % rules['lt']
                return True

        if rules.get('format', False):
            if not match(rules['format'], data):
                errors[field] = 'Invalid format'
                return True

        if rules.get('in', False):
            if data not in rules['in']:
                errors[field] = 'Invalid'
                return True

        return False

    @staticmethod
    def _convert(data):
        """Check if given data is a string, and loads it."""
        if isinstance(data, (str, dict, list)):
            if isinstance(data, (str, unicode)):
                try:
                    return (loads(data), False)
                except JSONDecodeError:
                    return (False, '1')
            else:
                return (data, False)
        return (False, '2')
