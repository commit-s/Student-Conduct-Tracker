import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Review
from App.controllers import (
    create_student,
    create_staff,
    get_staff_by_UniId,
    get_staff_by_id,
    get_student_by_id,
    get_student_by_UniId,
    create_review,
    delete_review,
    get_total_review_points,
    get_review
)
'''
   Unit Tests
'''
class ReviewUnitTests(unittest.TestCase):

    def test_new_review(self):
        assert create_staff(UniId="816000000",firstname="Joe", lastname="Mama", email="joe.mama@sta.uwi.edu", password="joepass", faculty="Science & Technology") == True
        assert create_student(UniId="816032311", firstname="Billy", lastname="John", email="billy.john@my.uwi.edu", faculty="Science & Technology", admittedTerm="2022/2023", degree="BSc Computer Science", gpa=3.5) == True
        student = get_student_by_UniId("816032311")
        staff = get_staff_by_UniId("816000000")
        review = Review(staff=staff, student=student, course="COMP1600", isPositive=True, points=3, details="Billy is good.", studentSeen=False)
        assert review is not None

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

class ReviewIntegrationTests(unittest.TestCase):

    def test_create_review(self):
        assert create_staff(UniId="816000555", firstname="Joe", lastname="Mama", email="joe.mama2@sta.uwi.edu", password="joepass", faculty="Science & Technology") == True
        assert create_student(UniId="816032312", firstname="Billy", lastname="John", email="billy.john3@my.uwi.edu", faculty="Science & Technology", admittedTerm="2022/2023", degree="BSc Computer Science", gpa=3.5) == True
        student = get_student_by_UniId("816032312")
        staff = get_staff_by_UniId("816000555")
        assert create_review(staff=staff, student=student, course="COMP3600", isPositive=True, points=3, details="Billy is good.") == True

    def test_get_review(self):
        create_staff(UniId="816009999", firstname="Perm", lastname="Mohan", email="perm.mohan@sta.uwi.edu", password="permpass", faculty="Science & Technology")
        create_student(UniId="816008888", firstname="Aarti", lastname="Sirju", email="aarti.sirju@my.uwi.edu", faculty="Science & Technology", admittedTerm="2022/2023", degree="BSc Computer Science", gpa=3.5)
        student = get_student_by_UniId("816008888")
        staff = get_staff_by_UniId("816009999")
        
        create_review(staff=staff, student=student, course="COMP3600", isPositive=True, points=3, details="Billy is good.")
        
        review = get_review(1)
        assert review is not None

    def test_get_total_points(self):
        review = get_review(1)
        assert get_total_review_points(review.studentID) != 0

    def test_delete_review(self):
        review = get_review(1)
        assert delete_review(review.ID) == True
