from App import get_student_by_id, Karma, get_karma_student
from App.controllers.AbstractCommand import AbstractCommand
from App.database import db

class AddKarma(AbstractCommand):
    def execute(self):
        student = get_student_by_id(self.student_id)
        assert student is not None
        old_karma = get_karma_student(student)
        old_karma.update_karma("+", self.karma_diff)
        db.session.update(old_karma)

        try:
            db.session.commit()
            return True
        except Exception as e:
            print(f"[AddKarma.execute] Error while increasing student {self.student_id}'s karma by {self.karma_diff}: {str(e)}")
            return False