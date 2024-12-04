from App.database import db
from .user import User


class Admin(User):
  __tablename__ = 'admin'
  ID = db.Column(db.Integer, db.ForeignKey('user.ID'), primary_key=True)

  __mapper_args__ = {"polymorphic_identity": "admin"}

  def __init__(self, UniId, firstname, lastname, email, password):
    super().__init__(UniId=UniId, firstname=firstname, lastname=lastname,  email=email, password=password)


  #return admin details on json format
  def to_json(self):
    return {
        "adminID": self.ID,
        "UniId": self.UniId,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email,
    }
  
  def __repr__(self):
    return f'<Admin {self.ID}: {self.email}>'
