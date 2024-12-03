from App.database import db
from .student import Student

MULTIPLIERS = {
  "academic": 0.45,
  "accomplishment": 0.35,
  "reviews": 0.2,
  "incident": -0.3,
}

class Karma(db.Model):
  __tablename__ = "karma"
  karmaID = db.Column(db.Integer, primary_key=True)
  points = db.Column(db.Float, nullable=False, default=0.0)
  academicPoints = db.Column(db.Float, nullable=False)
  accomplishmentPoints = db.Column(db.Float, nullable=False, default=0.0)
  incidentPoints = db.Column(db.Float, nullable=False, default=0.0)
  reviewsPoints = db.Column(db.Float, nullable=False, default=0.0)
  rank = db.Column(db.Integer, nullable=False, default=-99)
  studentID = db.Column(db.Integer, db.ForeignKey('student.ID', use_alter=True))

  def __init__(self, points, academicPoints, accomplishmentPoints,
               reviewsPoints, incidentPoints, rank, studentID):
    self.points = points
    self.academicPoints = academicPoints
    self.accomplishmentPoints = accomplishmentPoints
    self.reviewsPoints = reviewsPoints
    self.incidentPoints = incidentPoints
    self.rank = rank
    self.studentID = studentID

  def calculate_total_points(self):
    self.points = round(
      (self.academicPoints * MULTIPLIERS["academic"]) +
      (self.accomplishmentPoints * MULTIPLIERS["accomplishment"]) +
      (self.reviewsPoints * MULTIPLIERS["reviews"]) +
      (self.incidentPoints * MULTIPLIERS["incident"]), 2
    )