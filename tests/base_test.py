"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    # runs for every test class
    @classmethod
    def setUpClass(cls):
        # use postgres or mysql in production, sqllite doe not enfore constraints (foreign keys, primary keys)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['DEBUG'] = False
        with app.app_context():
            db.init_app(app)

    # runs for every test method
    def setUp(self):
        # Make sure database exists
        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()
