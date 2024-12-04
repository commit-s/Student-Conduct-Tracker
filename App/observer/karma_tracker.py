from App.observer.observer import Observer
from App.controllers.karma import get_karma, calculate_karma_points
from App.database import db

class KarmaTracker(Observer):
    # List of event names relevant to KarmaTracker
    RELEVANT_EVENTS = {"new_review", "new_incident", "new_academic"}

    def update(self, event):
        if event.name not in self.RELEVANT_EVENTS:
            return

        student_id = event.student_id
        karma = get_karma(student_id)

        if karma:
            # Calculate and update all karma-related points based on the event
            success = calculate_karma_points(student_id)
            if success:
                print(f"[KarmaTracker] Updated karma for student {student_id} after '{event.name}' event.")
            else:
                print(f"[KarmaTracker] Failed to update karma for student {student_id}.")
        else:
            print(f"No karma record found for student ID: {student_id}")
