
[![Build Status](https://travis-ci.org/sonic182/json_validator.svg?branch=master)](https://travis-ci.org/sonic182/json_validator)
[![Coverage Status](https://coveralls.io/repos/github/sonic182/json_validator/badge.svg?branch=master)](https://coveralls.io/github/sonic182/json_validator?branch=master)
[![PyPI version](https://badge.fury.io/py/sonic182_json_validator.svg)](https://badge.fury.io/py/sonic182_json_validator)
# Json Validator

A custom json validator.

* Works with Python 2.7.x, 3.5.x, 3.6. It may work with 3.7.X
* Constrains based on python types.


```python
from json_validator.validators import JsonValidator

constrain = {
      'string': {},  # str by default.
      'integer': {'type': int},
      'float': {'type': float},
      'boolean': {'type': bool},
      'json': { 'type': dict },
      'list': { 'type': list},
      'extra_1': {},
      'extra_2': {},
  }
  json = {
      'string': 'foo',
      'integer': 42,
      'float': 1.10,
      'boolean': True,
      'json': {},
      'list': []
  }
  # accepts json string, dict and array.
  res, err = JsonValidator(constrain).validate(json)
  res == json  # => True
  err == {'extra_1': 'Missing field', 'extra_2': 'Missing field'}  # => True

```

See all rules for fields [here](https://github.com/sonic182/json_validator/blob/master/tests/validator.py).

# Install

```bash
pip install sonic182_json_validator
```

# Development

Install packages with pip-tools:
```bash
pip install pip-tools
pip-compile
pip-compile dev-requirements.in
pip-sync requirements.txt dev-requirements.txt
```

# TODO

* Optional error messages defined in constrain (for i18n and more).
* Maybe change recursive algorithm with secuential version.

# Contribute

1. Fork
2. create a branch `feature/your_feature`
3. commit - push - pull request

Thanks :)
