"""Setup module."""

from setuptools import setup
from pip.req import parse_requirements

REQS = [str(ir.req) for ir in parse_requirements(
    'requirements.txt', session='hack')]
REQS2 = [str(ir.req) for ir in parse_requirements(
    'dev-requirements.txt', session='hack')]

setup(
    name='sonic182_json_validator',
    version='0.0.1',
    description='A custom json validator',
    author='Johanderson Mogollon',
    author_email='johanderson@mogollon.com.ve',
    url='https://github.com/sonic182/json_validator',
    license='MIT',
    setup_requires=['pytest-runner'],
    test_requires=['pytest'],
    install_requires=REQS,
    extras_require={
        'dev': REQS2,
        'test': [
            'pytest',
            'coverage'
        ]
    }
)
