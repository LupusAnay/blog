import pytest

from app import create_app, ConfigNames
from app.models import db


class BaseTestCase:
    @pytest.fixture
    def app(self):
        app = create_app(ConfigNames.testing)

        with app.app_context():
            db.create_all()

            yield app

            db.drop_all()

    @pytest.fixture
    def client(self, app):
        return app.test_client()
