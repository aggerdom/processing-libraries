from setuptools import setup

setup(
    name='processing_utilites',
    version='0.1',
    install_requires=['pytest'],
    packages=['processing_utilities'],
    package_data={'processing_utilities': ['tests/*', 'tests/**/*']},
)
