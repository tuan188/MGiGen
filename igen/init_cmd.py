# coding=utf-8

from .pb import pasteboard_write
from .model import InitModel
from .command import Command


class InitCommand(Command):

    def __init__(self, model_string):
        super(InitCommand, self).__init__()
        self.model_string = model_string

    def create_init(self, print_result):
        try:
            model = InitModel.from_string(self.model_string)
        except Exception:
            print("The model in the pasteboard is invalid.")
            exit(1)

        output = model.create_init()
        if print_result:
            print()
            print(output)
            print()

        pasteboard_write(output)
        print('The result has been copied to the pasteboard.')
