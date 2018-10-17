# coding=utf-8

from .pb import pasteboard_write
from .vm import UnitTest
from .command import Command

class UnitTestCommand(Command):
	def __init__(self, vm_text):
		super(UnitTestCommand, self).__init__()
		self.vm_text = vm_text

	def create_tests(self, print_result):
		output = UnitTest(self.vm_text).create_tests()
		if print_result:
			print()
			print(output)
			print()
		pasteboard_write(output)
		print('The result has been copied to the pasteboard.')
