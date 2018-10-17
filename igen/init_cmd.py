# coding=utf-8

from .pb import pasteboard_write
from .model import InitModel
from .command import Command

class InitCommand(Command):

	def __init__(self, model_text):
		super(InitCommand, self).__init__()
		self.model_text = model_text
		
	def create_init(self, print_result):
		output = InitModel(self.model_text).create_init()
		if print_result:
			print()
			print(output)
			print()
		pasteboard_write(output)
		print('The result has been copied to the pasteboard.')

