import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Staff
from App.controllers import (
    create_staff,
    get_staff_by_id,
    get_staff_by_UniId,
    staff_create_review,
    staff_edit_review,
    create_student,
    get_student_by_UniId,
    get_review
)
'''
   Unit Tests
'''
class StaffUnitTests(unittest.TestCase):

    def test_new_staff(self):
        staff = Staff(UniId="816000011",firstname="Joe", lastname="Joseph", email="joe.joseph@sta.uwi.edu", password="joepass", faculty="Science & Technology")
        assert staff.UniId == "816000011"

    def test_get_json(self):
        staff = Staff(UniId="816005555",firstname="Joe", lastname="Mama", email="joe.mama3@sta.uwi.edu", password="joepass", faculty="Science & Technology")
        staff_json = staff.to_json()
        self.assertDictEqual(staff_json, {
                "StaffID": None,
                "UniId": "816005555",
                "firstname": "Joe",
                "lastname": "Mama",
                "email": "joe.mama3@sta.uwi.edu",
                "faculty": "Science & Technology",
                "reviews": [],
                "reports": []
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

class StaffIntegrationTests(unittest.TestCase):

    def test_create_staff(self):
        assert create_staff(UniId="816000222", firstname="Joe", lastname="Mamaz", email="joe.mamaz@sta.uwi.edu", password="joepass", faculty="Science & Technology") == True

    def test_get_staff_by_id(self):
        staff = get_staff_by_id(1)
        assert staff is not None

    def test_get_staff_by_UniId(self):
        staff = get_staff_by_UniId("816000222")
        assert staff is not None

    def test_staff_create_review(self):
        assert create_student(
                 UniId='816031161',
                 firstname="Billy",
                 lastname="John",
                 email="billy@example.com",
                 faculty="Science & Technology",
                 admittedTerm="2022/2023",
                 degree="BSc Computer Science",
                 gpa=2.9) == True
        student = get_student_by_UniId("816031161")
        staff = get_staff_by_id(1)
        assert staff is not None
        assert staff_create_review(staff=staff, student=student, course="COMP1600", isPositive=True, points=3, details="Billy is good.") == True

    def test_staff_edit_review(self):
        review = get_review(1)
        assert review is not None
        assert staff_edit_review(review.ID, "Billy is very good") == True