from .subject import Subject
from .karma_tracker import KarmaTracker

# Initialize the subject and observers
subject = Subject()
karma_tracker = KarmaTracker()

# Attach the observers to the subject
subject.attach(karma_tracker)


# Expose these instances for import
__all__ = ["subject", "karma_tracker"]