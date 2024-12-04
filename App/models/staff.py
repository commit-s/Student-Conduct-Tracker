from App.database import db
from .user import User
from .student import Student


class Staff(User):
  __tablename__ = 'staff'
  ID = db.Column(db.Integer, db.ForeignKey('user.ID'), primary_key=True)
  faculty = db.Column(db.String(120), nullable=False)
  reviews = db.relationship('Review', backref='staffReviews', lazy='joined')
  reports = db.relationship('IncidentReport', backref='staffReports', lazy='joined')

  __mapper_args__ = {"polymorphic_identity": "staff"}

  def __init__(self, UniId, firstname, lastname, email, password, faculty):
    super().__init__(UniId=UniId, firstname=firstname, lastname=lastname, email=email, password=password)
    self.faculty=faculty
    self.reviews = []
    self.reports = []

  #return staff details on json format
  def to_json(self):
    return {
        "StaffID": self.ID,
        "UniId": self.UniId,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "email": self.email,
        "faculty":  self.faculty,
        "reviews": [review.to_json() for review in self.reviews],
        "reports": [report.to_json() for report in self.reports]
    }

  def __repr__(self):
    return f'<Staff {self.ID}: {self.email}>'
