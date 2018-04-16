"""Setup for decision tree module."""
from setuptools import setup


extra_packages = {
    'testing': ['pytest']
}


setup(
    name='Predicting Equipment Failure',
    description='Project aiming to predict equipment failure.',
    version=0.0,
    author='Kurt Maurer',
    author_email='kurtrm@gmail.com',
    extras_require=extra_packages
)
