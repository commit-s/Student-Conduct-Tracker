from App.models import Admin
from App.database import db 
from App.controllers import (
    create_staff,
    create_student,
)

def create_admin(UniId, firstname, lastname, email, password):
  newAdmin = Admin(UniId, firstname, lastname, email, password)
  db.session.add(newAdmin)
  try:
    db.session.commit()
    return True
  except Exception as e:
    print("[admin.create_admin] Error occurred while creating new admin: ", str(e))
    db.session.rollback()
    return False
  
def get_admin_by_UniId(UniId):
    return Admin.query.filter_by(UniId=UniId).first()
    
def add_staff(UniId, firstname, lastname, email, password, faculty):
    if create_staff(UniId, firstname, lastname, email, password, faculty):
        return True
    else:
        print("[admin.add_teacher] Error occurred while creating new staff: ")
        return False

def add_student(UniId, firstname, lastname, email, faculty, admittedTerm, degree, gpa):
    if create_student(UniId, firstname, lastname, email, faculty, admittedTerm, degree, gpa):
        return True
    else:
        print("[admin.add_student] Error occurred while creating new student: ")
        return False
