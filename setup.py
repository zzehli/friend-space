"""
Friend Space python package configuration.
"""

from setuptools import setup

setup(
    name='friendspace',
    version='0.1.0',
    packages=['friendspace'],
    include_package_data=True,
    install_requires=[
        'arrow',
        'bs4',
        'Flask',
        'html5validator',
        'pycodestyle',
        'pydocstyle',
        'pylint',
        'pytest',
        'requests',
        'selenium',
    ],
    python_requires='>=3.8',
)
