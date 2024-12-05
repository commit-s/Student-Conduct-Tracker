from App.database import db
from sqlalchemy import text
from .student import create_student, get_student_by_UniId
from .user import User
from .staff import create_staff, get_staff_by_UniId
from .admin import create_admin, get_admin_by_UniId
from .review import create_review

def reset_database():
    try:
        # Explicitly drop tables in the correct order
        db.session.execute(text('DROP TABLE IF EXISTS karma CASCADE;'))
        db.session.execute(text('DROP TABLE IF EXISTS student CASCADE;'))
        db.session.execute(text('DROP TABLE IF EXISTS other_table_name CASCADE;'))  # Add other tables as needed
        
        # Recreate the schema
        db.session.execute(text('DROP SCHEMA IF EXISTS public CASCADE;'))
        db.session.execute(text('CREATE SCHEMA public;'))

        # Recreate all tables
        db.create_all()
        db.session.commit()
        print("Database reset successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error while resetting the database: {e}")

def initialize():
    # Drop all foreign key constraints (postgres is very strict)
    #reset_database()

    # Recreate all tables
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
    create_review(staff, student1, "COMP1600", True, 5, "Behaves very well in class!")

    create_admin(
                UniId="8160332315",
                firstname="Admin",
                lastname="Main",
                email="admin@sta.uwi.edu",
                password="password")