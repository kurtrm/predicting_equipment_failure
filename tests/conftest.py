"""
Test fixtures.
"""
import pytest

from src import app, db

@pytest.fixture
def create_app():
    import pdb; pdb.set_trace()
    return app.config.from_object('project.config.TestingConfig')
