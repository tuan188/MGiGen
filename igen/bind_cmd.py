# coding=utf-8

from .pb import pasteboard_write
from .vm import BindViewModel
from .command import Command

class BindViewModelCommand(Command):
	def __init__(self, vm_text):
		super(BindViewModelCommand, self).__init__()
		self.vm_text = vm_text

	@classmethod
	def description(cls):
		return "Create bindViewModel method for view controller from view model"

	@classmethod
	def name(cls):
		return "bind"

	def create_bind_view_model(self):
		# try:
		output = BindViewModel(self.vm_text).create_bind_view_model()
		pasteboard_write(output)
		print("The result has been copied to the pasteboard.")
		# except:
		# 	print("Invalid view model text in clipboard.")