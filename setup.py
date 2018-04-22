"""Setup module."""

import re
from setuptools import setup

RGX = re.compile('(\w+==[\d.]+)')


def read_file(filename):
    """Read file correctly."""
    with open(filename) as _file:
        return _file.read().strip()


def parse_requirements(filename):
    """Parse requirements from file."""
    return re.findall(RGX, read_file(filename)) or []


setup(
    name='sonic182_json_validator',
    version=read_file('VERSION'),
    description='A custom json validator',
    long_description=read_file('README.rst'),
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='json validator dictionary',
    setup_requires=['pytest-runner'],
    test_requires=['pytest'],
    install_requires=parse_requirements('requirements.txt'),
    extras_require={
        'dev': parse_requirements('dev-requirements.txt'),
        'test': parse_requirements('test-requirements.txt'),
    }
)
