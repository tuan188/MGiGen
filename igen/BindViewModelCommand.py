# coding=utf-8

from Pasteboard import pasteboard_write
from ViewModel import BindViewModel

class BindViewModelCommand(object):
	def __init__(self, vm_text):
		super(BindViewModelCommand, self).__init__()
		self.vm_text = vm_text

	def create_bind_view_model(self):
		# try:
		output = BindViewModel(self.vm_text).create_bind_view_model()
		pasteboard_write(output)
		print("Text has been copied to clipboard.")
		# except:
		# 	print("Invalid view model text in clipboard.")