import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Admin
from App.controllers import (
    add_staff,
    add_student,
)
'''
   Unit Tests
'''
class AdminUnitTests(unittest.TestCase):
    
    def test_new_admin(self):
        newAdmin = Admin(UniId="816032344", firstname="Phil", lastname="Smith", email="phil.smith@sta.uwi.edu",  password="philpass")
        assert newAdmin.UniId == "816032344"
    
    def test_to_json(self):
        newAdmin = Admin(UniId="816032344", firstname="Phil", lastname="Smith", email="phil.smith@sta.uwi.edu",  password="philpass")
        newAdmin_json = newAdmin.to_json()
        self.assertDictEqual(newAdmin_json,{
            "adminID": None,
            "UniId": "816032344",
            "firstname": "Phil",
            "lastname": "Smith",
            "email": "phil.smith@sta.uwi.edu",
        })

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

class AdminIntegrationTests(unittest.TestCase):

    def test_add_staff(self):
        assert add_staff(UniId="816032311", firstname="John", lastname="Doe", email="john.doe@sta.uwi.edu", password="johnpassword", faculty="Science & Technology") == True
        

    def test_add_student(self):
        assert add_student(UniId="816032311", firstname="Alice", lastname="Smith", email="alice.smith@my.uwi.edu", faculty="Science & Technology", admittedTerm="2022/2023", degree="BSc Computer Science (General)", gpa=3.5) == True