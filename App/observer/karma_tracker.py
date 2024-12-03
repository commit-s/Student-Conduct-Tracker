from App.observer.observer import Observer
from App.controllers.karma import (get_karma, calculate_review_points, calculate_accomplishment_points, 
                                   calculate_incident_points, update_total_points, calculate_ranks)
from App.database import db

class KarmaTracker(Observer):
    def update(self, event):
        student_id = event.student_id
        karma = get_karma(student_id)

        if karma:
            if event.name == "new_review":
                calculate_review_points(student_id)
            elif event.name == "new_accomplishment":
                calculate_accomplishment_points(student_id)
            elif event.name == "new_incident":
                calculate_incident_points(student_id)

            update_total_points(student_id)
            calculate_ranks()

            print(f"[KarmaTracker] Updated karma for student {student_id} after '{event.name}' event.")
        else:
            print(f"No karma record found for student ID: {student_id}")
