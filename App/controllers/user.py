from App.models import User, Student
from App.database import db

def create_user(UniId, firstname, lastname, email, password):
    newuser = User(UniId=UniId, firstname=firstname ,lastname=lastname, email=email, password=password)
    db.session.add(newuser)
    try:
        db.session.commit()
        return newuser
    except Exception as e:
        print("[user.create_user] Error occurred while creating new user: ", str(e))
        db.session.rollback()
        return None
    

def get_user_by_uniId(UniId):
    user = User.query.filter_by(UniId=UniId).first()
    if user:
        return user
    else:
        return None

def get_user(id):
    user = User.query.get(id)
    if user:
        return user
    else:
        return None

def get_user_student(student):
  user = User.query.get(student.ID)
  if user:
      return user
  else:
      return None

def get_all_users():
    users = User.query.all()
    if users:
        return users
    else:
        return []

def get_all_users_json():
    users = User.query.all()
    # users = Student.query.all()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users