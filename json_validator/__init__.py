"""Json schema validator module."""
# -*- coding: utf-8 -*-

from re import match
from datetime import datetime

from json import loads

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

try:
    UNICODE = unicode
except NameError:
    unicode = str

ERRORS = {
    '1': 'INVALID PAYLOAD',
    '2': 'INVALID DATA TYPE'
}


class JsonValidator:
    """Json Schema validator."""

    def __init__(self, constrain, lazy=False, decode_error=None,
                 data_error=None):
        """Set the constrain in object."""
        if not isinstance(constrain, dict):
            raise AttributeError('constrain must be a dict')
        self.constrain = constrain
        self.lazy = lazy
        self.decode_error = decode_error
        self.data_error = data_error

    def validate(self, data, constrain=None):
        """Validate incoming data."""
        res = {}
        errors = {}
        data, err = self._convert(data)

        if err and err in ('1', '2'):
            return (None, (self.decode_error or {
                'payload': ERRORS.get(err, '')}))

        stack = []
        constrain = constrain or self.constrain
        my_field = ''

        if constrain:
            stack.append((res, errors, my_field, data, constrain))

        while stack:
            temp_res, temp_errors, my_field, data, constrain = stack.pop()

            if constrain is None:
                continue

            for key, rule in constrain.items():
                field = my_field + '.' + key if my_field else key

                if key not in data:
                    if rule.get('default', False):
                        if callable(rule['default']):
                            temp_res[key] = rule['default']()
                        else:
                            temp_res[key] = rule['default']
                    else:
                        temp_errors[field] = rule.get('error', 'Missing field')
                        if self.lazy:
                            break
                else:
                    self._key_match(data[key], rule, key, field, temp_res,
                                    temp_errors, stack)
                    if temp_errors and self.lazy:
                        self.clean_data(res)
                        return res, errors

        self.clean_data(errors)
        self.clean_data(res)
        return res, errors

    def _key_match(self, my_obj, my_rules, my_key, my_field, my_res, my_errors,
                   stack):
        """Validate object with rueles."""
        matcheds = [(my_obj, my_rules, my_key, my_field, my_res, my_errors)]

        while matcheds:
            obj, rules, key, field, res, errors = matcheds.pop()
            splitted = field.split('.')
            err_field = field

            try:
                err_field = int(
                    splitted[len(splitted) - 1]) if splitted else field
            except ValueError:
                pass

            if not isinstance(obj, (rules.get('type', str),
                                    rules.get('type', unicode))):
                if self.special_types(obj, rules, key, err_field, res, errors):
                    if errors and self.lazy:
                        return
                else:
                    errors[err_field] = rules.get(
                        'type_error', 'Bad data type')
                    if self.lazy:
                        return

            elif self._extra_validations(obj, rules, errors, field):
                if self.lazy:
                    return

            elif isinstance(obj, dict):
                res[key] = {}
                errors[key] = {}
                stack.append((res[key], errors[key], field, obj,
                              rules.get('properties', None)))

            elif isinstance(obj, list):
                res[key] = []
                errors[key] = []
                my_field2 = field
                for ind, item in enumerate(obj):
                    field = my_field2
                    field += '.{}'.format(ind)
                    res[key].append(None)
                    errors[key].append(None)

                    matcheds.append((item, rules.get('items', {}), ind, field,
                                     res[key], errors[key]))

            else:
                res[key] = obj

        return res, errors

    @classmethod
    def clean_data(cls, error, key=None, parent=None):
        """Clean empty errors."""
        if isinstance(error, dict):
            items = error.copy().items()
            for _key, _value in items:
                cls.clean_data(_value, _key, error)

        elif isinstance(error, list):
            aux = len(error)
            while aux > 0:
                aux -= 1
                cls.clean_data(error[aux], aux, error)

        if not error and parent:
            if isinstance(parent, dict):
                del parent[key]
            else:
                parent.pop(key)

    @staticmethod
    def special_types(obj, rules, key, field, res, errors):
        """Validate if special type retrieved."""
        if rules.get('type', str) == datetime:
            if rules.get('dformat', False):
                try:
                    res[key] = datetime.strptime(obj, rules['dformat'])
                except ValueError:
                    errors[field] = rules.get(
                        'dformat_error', 'Invalid format')
            else:
                raise AttributeError('Missing `dformat` on datetime rule')
            return True
        return False

    @staticmethod
    def _extra_validations(data, rules, errors, field):
        """Extras validations."""
        if isinstance(data, (int, float)):
            if rules.get('gt', False) and not data > rules['gt']:
                errors[field] = rules.get(
                    'gt_error', 'Not greater than {limit}').format(
                        value=data, limit=rules['gt'])
                return True

            elif rules.get('lt', False) and not data < rules['lt']:
                errors[field] = rules.get(
                    'lt_error', 'Not less than {limit}').format(
                        value=data, limit=rules['lt'])
                return True

        if rules.get('format', False):
            if not match(rules['format'], data):
                errors[field] = rules.get(
                    'format_error', 'Invalid format')
                return True

        if rules.get('in', False):
            if data not in rules['in']:
                errors[field] = rules.get('in_error', 'Invalid')
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
