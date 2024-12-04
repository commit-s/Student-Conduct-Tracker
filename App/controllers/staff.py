from App.models import Staff
from App.database import db 
from .review import create_review, get_review

def create_staff(UniId, firstname, lastname, email, password, faculty):
    newStaff = Staff(UniId=UniId, firstname=firstname, lastname=lastname, email=email, password=password, faculty=faculty)
    db.session.add(newStaff)
    try:
        db.session.commit()
        return True
    except Exception as e:
        print("[staff.create_staff] Error occurred while creating new staff: ", str(e))
        db.session.rollback()
        return False

def get_staff_by_UniId(UniId):
    return Staff.query.filter_by(UniId=UniId).first()

def get_staff_by_id(id):
    return Staff.query.filter_by(ID=id).first()

def get_staff_by_name(firstname, lastname):
  return Staff.query.filter_by(firstname=firstname, lastname=lastname).first()

def staff_edit_review(id, details):
    review = get_review(id)
    if review:
        review.details = details
        try:
            # Notify Observer Here
            db.session.commit()
            return True
        except Exception as e:
            print("[staff.staff_edit_review] Error occurred while editing review:", str(e))
            db.session.rollback()
            return False
    
    return False


def staff_create_review(staff, student, course, isPositive, points, details):
    return create_review(staff, student, course, isPositive, points, details)




