# coding=utf-8

from .pb import pasteboard_write
from .vm import UnitTest
from .command import Command

class UnitTestCommand(Command):
	def __init__(self, vm_text):
		super(UnitTestCommand, self).__init__()
		self.vm_text = vm_text

	@classmethod
	def description(cls):
		return "Create Unit Tests from view model"

	@classmethod
	def name(cls):
		return "test"

	def create_tests(self):
		# try:
		output = UnitTest(self.vm_text).create_tests()
		pasteboard_write(output)
		print("Text has been copied to clipboard.")
		# except:
		# 	print("Invalid view model text in clipboard.")