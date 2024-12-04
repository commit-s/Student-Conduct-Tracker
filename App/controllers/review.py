from App.models import Review
from App.observer.events import Event
from App.database import db


def create_review(staff, student, course, isPositive, points, details):
  from App.observer.initialize import subject # decoupled to avoid circular import error

  newReview = Review(staff=staff, student=student, course=course, isPositive=isPositive, points=points, details=details, studentSeen=False)
  db.session.add(newReview)

  try:
    db.session.commit()
    event = Event(name="new_review", student_id=student.ID) # Send event to observer
    subject.notify(event)
    return True
  except Exception as e:
    print("[review.create_review] Error occurred while creating new review: ",
          str(e))
    db.session.rollback()
    return False


def delete_review(reviewID):
  review = Review.query.filter_by(ID=reviewID).first()
  if review:
    db.session.delete(review)
    try:
      db.session.commit()
      return True
    except Exception as e:
      print("[review.delete_review] Error occurred while deleting review: ",
            str(e))
      db.session.rollback()
      return False
  else:
    return False

def get_total_review_points(studentID):
  reviews = Review.query.filter_by(studentID=studentID).all()
  if reviews:
      total_points = 0
      review_count = 0

      for review in reviews:
          
          capped_points = max(min(review.points, 30), -30) # Cap points between -30 and 30
          total_points += capped_points / 30 # Normalize to a base value of 1
          review_count += 1 if -30 <= capped_points <= 30 else 0 # Only count reviews after applying the threshold

      # Avoid division by zero
      if review_count == 0:
          return 0

      # Normalize to a scale of 0-100
      return round(100 * total_points / review_count, 2)
  
  return 0


def get_review(id):
  return Review.query.get(id)
