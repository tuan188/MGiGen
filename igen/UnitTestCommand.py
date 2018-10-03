# coding=utf-8

from Pasteboard import pasteboard_write
from ViewModel import UnitTest

class UnitTestCommand(object):
	def __init__(self, vm_text):
		super(UnitTestCommand, self).__init__()
		self.vm_text = vm_text

	def create_tests(self):
		# try:
		output = UnitTest(self.vm_text).create_tests()
		pasteboard_write(output)
		print("Text has been copied to clipboard.")
		# except:
		# 	print("Invalid view model text in clipboard.")