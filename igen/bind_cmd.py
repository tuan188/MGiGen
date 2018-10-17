# coding=utf-8

from .pb import pasteboard_write
from .vm import BindViewModel
from .command import Command

class BindViewModelCommand(Command):
	def __init__(self, vm_text):
		super(BindViewModelCommand, self).__init__()
		self.vm_text = vm_text

	def create_bind_view_model(self, print_result):
		output = BindViewModel(self.vm_text).create_bind_view_model()
		if print_result:
			print()
			print(output)
			print()
		pasteboard_write(output)
		print('The result has been copied to the pasteboard.')
		