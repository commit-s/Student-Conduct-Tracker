from abc import ABC, abstractmethod
from App.controllers.Command import Command

class AbstractCommand(ABC, Command):
    def __init__(self, student, karma_change):
        self.student_id = student
        self.karma_diff = karma_change

    @abstractmethod
    def execute(self):
        pass