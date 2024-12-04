from App.models import Karma
from App.database import db
from .review import (get_total_review_points)
from .incident import (get_total_incident_points)
from .transcript import (calculate_academic_score)

def get_karma(studentID):
  return Karma.query.filter_by(studentID=studentID).first()

def create_karma(studentID):
  newKarma = Karma(points=0.0, academicPoints=0.0, reviewsPoints=0.0, incidentPoints=0.0, studentID=studentID)
  db.session.add(newKarma)
  try:
    db.session.commit()
    return True
  except Exception as e:
    print("[karma.create_karma] Error occurred while creating new karma: ", str(e))
    db.session.rollback()
    return False


def calculate_karma_points(studentID):
  """
    Calculate and update all karma-related points for a student.
    This includes academic, review, and incident points, as well as the total.
  """
  karma = get_karma(studentID)
  if not karma:
    print(f"[karma.calculate_karma_points] No Karma record found for sutdent ID: {studentID}")
    return False
  
  try:
    # Fetch and update inidividual point categories
    karma.academicPoints = calculate_academic_score(studentID)
    karma.reviewsPoints = get_total_review_points(studentID)
    karma.incidentPoints = get_total_incident_points(studentID)

    # Recalculate total points using the model's method
    karma.calculate_total_points()

    db.session.commit()
    return True
  except Exception as e:
    print(f"[karma.calculate_karma_points] Error updating karma points: {e}")
    db.session.rollback()
    return False