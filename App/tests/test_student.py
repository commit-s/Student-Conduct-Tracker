import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import Student
from App.controllers import (
    create_student,
    get_karma,
    get_student_by_id,
    get_student_by_UniId,
    get_students_by_degree,
    get_students_by_faculty,
    get_all_students_json,
)

'''
   Unit Tests
'''
class StudentUnitTests(unittest.TestCase):

    def test_new_student(self):
        student = Student(UniId="816032311", firstname="Billy", lastname="John", email="billy.john@my.uwi.edu", faculty="Science & Technology", admittedTerm="2022/2023", degree="BSc Computer Science", gpa=3.5)
        assert student.UniId == "816032311"

    def test_get_json(self):
        student = Student(UniId="816032311", firstname="Billy", lastname="John", email="billy.john@my.uwi.edu", faculty="Science & Technology", admittedTerm="2022/2023", degree="BSc Computer Science", gpa=3.5)
        karma = get_karma(student.karmaID)
        student_json = student.to_json(karma)
        self.assertDictEqual(student_json, {"studentID": None,
                                            "UniId": "816032311",
                                            "firstname": "Billy",
                                            "lastname": "John",
                                            "gpa": 3.5,
                                            "email": "billy.john@my.uwi.edu",
                                            "faculty": "Science & Technology",
                                            "degree": "BSc Computer Science",
                                            "admittedTerm": "2022/2023",
                                            "reviews": [],
                                            "incidents": [],
                                            "grades": [],
                                            "transcripts": [],
                                            "karmaScore": None
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

class StudentIntegrationTests(unittest.TestCase):

    def test_create_student(self):
        assert create_student(UniId="816032311", firstname="Billy", lastname="John", email="billy.john@my.uwi.edu", faculty="Science & Technology", admittedTerm="2022/2023", degree="BSc Computer Science", gpa=3.5) == True
        
    def test_get_student_by_id(self):
        student = get_student_by_id(1)
        assert student is not None
    
    def test_get_student_by_UniId(self):
        student = get_student_by_UniId("816032311")
        assert student is not None

    def test_get_studens_by_degree(self):
        students = get_students_by_degree("BSc Computer Science")
        assert students != []

    def test_get_students_by_faulty(self):
        students = get_students_by_faculty("Science & Technology")
        assert students != []
    
    def test_get_students_json(self):
        students = get_all_students_json()
        assert students != []