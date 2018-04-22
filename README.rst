|Build Status| |Coverage Status| |PyPI version| # Json Validator

A json validator focused on speed.

-  Not recursion
-  Works with Python 2.7.x, 3.4.x, 3.5.x, 3.6. It may work with 3.7.X
-  Constrains based on python types.
-  Lazy Validation
-  Constrain definitions with python types

.. code:: python

    from json_validator import JsonValidator

    constrain = {
          'string': {},  # str by default.
          'integer': {'type': int},
          'float': {'type': float},
          'boolean': {'type': bool},
          'json': {'type': dict },
          'list': {'type': list},
          'extra_1': {},
          'extra_2': {},
      }
      json = {
          'string': 'foo',
          'integer': 42,
          'float': 1.10,
          'boolean': True
      }
      # accepts json string, dict and lists.
      res, err = JsonValidator(constrain).validate(json)
      res == json  # => True
      err == {'extra_1': 'Missing field', 'extra_2': 'Missing field'}  # => True

See all rules for fields `here`_.

Install
=======

.. code:: bash

    pip install sonic182_json_validator

Development
===========

Install packages with pip-tools:

.. code:: bash

    pip install pip-tools
    pip-compile
    pip-compile dev-requirements.in
    pip-sync requirements.txt dev-requirements.txt

TODO
====

-  Documentation about rules.

Contribute
==========

1. Fork
2. create a branch ``feature/your_feature``
3. commit - push - pull request

Thanks :)

.. _here: https://github.com/sonic182/json_validator/blob/master/tests/test_validator.py

.. |Build Status| image:: https://travis-ci.org/sonic182/json_validator.svg?branch=master
   :target: https://travis-ci.org/sonic182/json_validator
.. |Coverage Status| image:: https://coveralls.io/repos/github/sonic182/json_validator/badge.svg?branch=master
   :target: https://coveralls.io/github/sonic182/json_validator?branch=master
.. |PyPI version| image:: https://badge.fury.io/py/sonic182_json_validator.svg
   :target: https://badge.fury.io/py/sonic182_json_validator
