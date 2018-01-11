"""Setup module."""

from setuptools import setup
from pip.req import parse_requirements

REQS = [str(ir.req) for ir in parse_requirements(
    'requirements.txt', session='hack')]
REQS2 = [str(ir.req) for ir in parse_requirements(
    'dev-requirements.txt', session='hack')]

with open('VERSION') as _file:
    VERSION = _file.read()

setup(
    name='sonic182_json_validator',
    version=VERSION,
    description='A custom json validator',
    author='Johanderson Mogollon',
    author_email='johanderson@mogollon.com.ve',
    url='https://github.com/sonic182/json_validator',
    license='MIT',
    packages=['json_validator'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='json validator dictionary',
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
