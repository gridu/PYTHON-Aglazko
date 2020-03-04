"""pytests fixtures"""

import pytest
from app.main import create_app


@pytest.fixture(scope='session')
def test_app():
    """This fixture creates test flask application"""
    app = create_app()
    return app


@pytest.fixture(scope='function')
def client(test_app):
    """This fixture creates test client from test application that can perform
    requests like get, post etc"""
    client = test_app.test_client()
    return client
