import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User(UniId="816032311", firstname="Bob", lastname="Smith", email="bob@example.com", password="bobpass")
        assert user.UniId == "816032311"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User(UniId="816032311", firstname="Bob", lastname="Smith", email="bob@example.com", password="bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id": None, "UniId": "816032311", "firstname": "Bob", "lastname": "Smith", "email": "bob@example.com"})

    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User(UniId="816032311", firstname="Bob", lastname="Smith", email="bob@example.com", password=password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User(UniId="816032311", firstname="Bob", lastname="Smith", email="bob@example.com", password=password)
        assert user.check_password(password)

'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("816032311", "Bob", "Smith", "bob@example.com", "bobpass")
    assert login("bob@example.com", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        print(users_json)
        self.assertListEqual([{"id":1, 
            "UniId":"816032311", 
            "firstname":"Bob", 
            "lastname":"Smith", 
            "email":"bob@example.com"},
            {
            "id":2, 
            "UniId":"816032312", 
            "firstname":"Rick", 
            "lastname":"Grimes", 
            "email":"rick@example.com"
            }], users_json)

    def test_create_user(self):
        user = create_user("816032312", "Rick", "Grimes", "rick@example.com", "rickpass")
        assert user.UniId == "816032312"