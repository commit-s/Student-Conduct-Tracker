from App.database import db
from .student import create_student, get_student_by_UniId
from .user import User
from .staff import create_staff, get_staff_by_UniId
from .admin import create_admin, get_admin_by_UniId
from .review import create_review

def initialize():
    db.drop_all()
    db.create_all()
    
    #Creating Students
    create_student(
                UniId='816031609',
                firstname="Brian",
                lastname="Cheruiyot",
                email="brian.cheruiyot@my.uwi.edu",
                faculty="Science & Technology",
                admittedTerm="2021/2022",
                degree="Bachelor of Computer Science (General)",
                gpa=0)
    
    #Creating staff
    create_staff(
                UniId="816032312",
                firstname="Tim",
                lastname="Long",
                email="tim.long@sta.uwi.edu",
                password="timpass",
                faculty="Science & Technology")

    create_staff(
                UniId="816032313",
                firstname="Vijayanandh",
                lastname="Rajamanickam",
                email="vijayanandh.rajamanickam@sta.uwi.edu",
                password="vijaypass",
                faculty="Science & Technology")

    create_staff(
                UniId="816032314",
                firstname="Permanand",
                lastname="Mohan",
                email="permanand.mohan@sta.uwi.edu",
                password="permpass",
                faculty="Science & Technology")

    
    staff = get_staff_by_UniId("816032314")
    student1 = get_student_by_UniId("816031609")
    print(staff, student1)
    create_review(staff, student1, "COMP1600", True, 5, "Behaves very well in class!")

    create_admin(
                UniId="8160332315",
                firstname="Admin",
                lastname="Main",
                email="admin@sta.uwi.edu",
                password="password")