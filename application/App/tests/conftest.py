import pytest
from flask import template_rendered
from App import create_app
from App.models import db
from flask_sqlalchemy import SQLAlchemy

@pytest.fixture(scope="module")
def app():
    app = create_app(env="TESTING")
    app.config["TESTING"] = True
    app.testing = True

    with app.app_context():
        db.create_all()

    yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture(scope="module")
def test_client(app):
    with app.test_client() as testing_client:
        yield testing_client

@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)