import pytest
from app.main import create_app


@pytest.fixture(scope='session')
def test_app():
    app = create_app()
    return app


@pytest.fixture(scope='function')
def client(test_app):
    client = test_app.test_client()
    return client
