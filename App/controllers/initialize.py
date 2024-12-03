from App.database import db
from .student import create_student, get_student_by_UniId, get_all_students
from .staff import create_staff, get_staff_by_id
from .admin import create_admin
from .review import create_review
from .karma import create_karma, get_karma

def initialize():
    db.drop_all()
    db.create_all()
    
    #commit -s team
    create_student(
                firstname="Jonathan",
                lastname="Joseph",
                email="jonathan.joseph2@my.uwi.edu",
                faculty="FST",
                admittedTerm="2021/2022",
                UniId="816032311",
                degree="Bachelor of Computer Science (General)",
                gpa="")

    #Creating staff
    create_staff(username="tim",
                firstname="Tim",
                lastname="Long",
                email="",
                password="timpass",
                faculty="")

    create_staff(username="vijay",
                firstname="Vijayanandh",
                lastname="Rajamanickam",
                email="Vijayanandh.Rajamanickam@sta.uwi.edu",
                password="vijaypass",
                faculty="FST")

    create_staff(username="permanand",
                firstname="Permanand",
                lastname="Mohan",
                email="Permanand.Mohan@sta.uwi.edu",
                password="password",
                faculty="FST")

    
    staff = get_staff_by_id(2)
    student1 = get_student_by_UniId(816032311)
    create_review(staff, student1, True, 5, "Behaves very well in class!")

    create_admin(username="admin",
                firstname="Admin",
                lastname="Admin",
                email="admin@example.com",
                password="password",
                faculty="FST")

    students = get_all_students()
    for student in students:
        if student:
            create_karma(student.ID)
            student.karmaID = get_karma(student.ID).karmaID
            db.session.commit()