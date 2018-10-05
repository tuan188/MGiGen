# coding=utf-8

from .pb import pasteboard_write
from .model import InitModel
from .command import Command

class InitCommand(Command):

	def __init__(self, model_text):
		super(InitCommand, self).__init__()
		self.model_text = model_text

	@classmethod
	def description(cls):
		return "Create init method for struct model"

	@classmethod
	def name(cls):
		return "init"
		
	def create_init(self):
		# try:
		output = InitModel(self.model_text).create_init()
		pasteboard_write(output)
		print("The result has been copied to the pasteboard.")
		# except:
		# 	print("Invalid model text in clipboard.")




