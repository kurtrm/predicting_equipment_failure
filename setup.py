"""Setup for decision tree module."""
from setuptools import setup


extra_packages = {
    'testing': ['pytest', 'selenium', 'bs4', 'requests']
}

description = '''Project leveraging machine learning to help determine if
electrical transformers will require more intensive maintenance schedules.'''

setup(
    name='predicting_equipment_failure',
    description=description,
    version=0.0,
    author='Kurt Maurer',
    author_email='kurtrm@gmail.com',
    install_requires=['numpy', 'pytz', 'pandas', 'sklearn', 'flask', 'psycopg2', 'scipy'],
    extras_require=extra_packages
)
