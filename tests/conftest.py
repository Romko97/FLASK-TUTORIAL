import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

# The app fixture will call the factory and pass test_config
# to configure the application and database for testing
# instead of using your local development configuration.

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp() 
    # creates and opens a temporary file,
    # returning the file object and the path to it. 
    # The DATABASE path is overridden so it points 
    # to this temporary path instead of the instance folder. 

    app = create_app({
        'TESTING': True, # tells Flask that the app is in test mode. 
        'DATABASE': db_path,
    })
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client() 
    # Tests will use the client
    # to make requests to the 
    # application without running the server.

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# For most of the views, a user needs to be logged in. 
# The easiest way to do this in tests is to make a POST request
# to the login view with the client. Rather than writing that out
# every time, you can write a class with methods to do that,
# and use a fixture to pass it the client for each test


class AuthActions():
    def __init__(self, client):
        self._client=client


    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)

# With the auth fixture, you can call auth.login() in a test to log in as 
# the test user, which was inserted as part of the test data in the app fixture.

# The register view should render successfully on GET. On POST with valid form 
# data, it should redirect to the login URL and the user’s data should be in the 
# database. Invalid data should display error messages.