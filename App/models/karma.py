from App.database import db
from .student import Student

MULTIPLIERS = {
  "academic": 0.2,
  "reviews": 0.4,
  "incident": -0.3,
}

class Karma(db.Model):
  __tablename__ = "karma"
  karmaID = db.Column(db.Integer, primary_key=True)
  points = db.Column(db.Float, nullable=False, default=0.0)
  academicPoints = db.Column(db.Float, nullable=False)
  incidentPoints = db.Column(db.Float, nullable=False, default=0.0)
  reviewsPoints = db.Column(db.Float, nullable=False, default=0.0)
  studentID = db.Column(db.Integer, db.ForeignKey('student.ID', name='fk_karma_student'),unique=True)

  def __init__(self, points, academicPoints, reviewsPoints, incidentPoints, studentID):
    self.points = points
    self.academicPoints = academicPoints
    self.reviewsPoints = reviewsPoints
    self.incidentPoints = incidentPoints
    self.studentID = studentID

  def calculate_total_points(self):
    self.points = round(
      (self.academicPoints * MULTIPLIERS["academic"]) +
      (self.reviewsPoints * MULTIPLIERS["reviews"]) +
      (self.incidentPoints * MULTIPLIERS["incident"]), 2
    )

  def to_json(self):
    return {
      "karmaID": self.karmaID,
      "score": self.points,
      "academicPoints": self.academicPoints, 
      "reviewPoints": self.reviewsPoints,
      "incidentPoints": self.incidentPoints,
      "studentID": self.studentID
    }