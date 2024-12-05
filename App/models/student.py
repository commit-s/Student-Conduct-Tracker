from App.database import db


class Student(db.Model):
  __tablename__ = "student"
  ID = db.Column(db.Integer,  primary_key=True)
  UniId = db.Column(db.String(10), nullable=False, unique=True)
  email = db.Column(db.String(120), nullable=False, unique=True)
  degree = db.Column(db.String(120), nullable=False)
  firstname = db.Column(db.String(120), nullable=False)
  lastname = db.Column(db.String(120), nullable=False)
  faculty = db.Column(db.String(120), nullable=False)
  degree = db.Column(db.String(120), nullable=False)
  admittedTerm = db.Column(db.String(120), nullable=False)
  gpa = db.Column(db.Float, nullable=True, default=0.0)

  reviews = db.relationship('Review', backref='studentReviews', lazy='joined')
  incidents = db.relationship('IncidentReport', backref='studentincidents', lazy='joined')
  grades = db.relationship('Grades', backref='studentGrades', lazy='joined')
  transcripts = db.relationship('Transcript', backref='student', lazy='joined')
  

  def __init__(self, UniId, firstname, lastname, email, faculty, admittedTerm, degree, gpa):
    self.firstname = firstname
    self.lastname = lastname
    self.email = email
    self.faculty = faculty
    self.admittedTerm = admittedTerm
    self.UniId = UniId
    self.degree = degree
    self.gpa = gpa
    self.reviews = []
    self.incidents = []
    self.grades = []
    self.transcripts = []

  def get_id(self):
    return self.ID

  # Gets the student details and returns in JSON format
  def to_json(self, karma):
    return {
        "studentID": self.ID,
        "UniId": self.UniId,
        "firstname": self.firstname,
        "lastname": self.lastname,
        "gpa": self.gpa,
        "email": self.email,
        "faculty": self.faculty,
        "degree": self.degree,
        "admittedTerm": self.admittedTerm,
        "reviews": [review.to_json() for review in self.reviews],
        "incidents": [incident.to_json() for incident in self.incidents],
        "grades": [grade.to_json() for grade in self.grades],
        "transcripts": [transcript.to_json() for transcript in self.transcripts],
        "karmaScore": karma.points if karma else None,
    }
