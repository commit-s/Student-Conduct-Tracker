from App.controllers.Command import Command

class KarmaModifierInvoker:
    def __init__(self):
        self.__command = None

    def get_command(self):
        return self.__command

    def setCommand(self, karmaCommand: Command):
        self.__command = karmaCommand

    def executeCommand(self):
        if self.__command:
            self.__command.execute()