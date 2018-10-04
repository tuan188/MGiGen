# coding=utf-8

import re
from .pb import pasteboard_write
from .command import Command
from .constants import SWIFT_TYPES_DEFAULT_VALUES, SWIFT_TYPES

class MockCommand(Command):
	def __init__(self, protocol_text):
		super(MockCommand, self).__init__()
		self.protocol_text = protocol_text

	@classmethod
	def description(cls):
		return "Create mock from protocol"

	@classmethod
	def name(cls):
		return "mock"

	def create_mock(self):
		# try:
		output = Mock(self.protocol_text).create_mock()
		pasteboard_write(output)
		print("Text has been copied to clipboard.")
		# except:
		# 	print("Invalid protocol text in clipboard.")


class Mock(object):

	class Function(object):
		def __init__(self, origin, name, return_type):
			super(Mock.Function, self).__init__()
			self.origin = origin
			self.name = name
			self.return_type = return_type

		def __str__(self):
			return self.origin

	def __init__(self, protocol_text):
		super(Mock, self).__init__()
		self.protocol_text = protocol_text

	def _get_protocol_name(self, str):
		regex = re.compile("protocol (\w+)")
		mo = regex.search(str)
		protocol_name = mo.group(1)
		if protocol_name.endswith("Type"):
			class_name = protocol_name[:-4]
		elif protocol_name.endswith("Protocol"):
			class_name = protocol_name[:-8]
		else:
			class_name = protocol_name
		return (protocol_name, class_name)

	def create_mock(self):
		str = self.protocol_text
		(protocol_name, class_name) = self._get_protocol_name(str)
		func_regex = re.compile("func (\w+)\(.*\)( -> (.*))?")
		funcs = [Mock.Function(f.group(), f.group(1), f.group(3)) for f in func_regex.finditer(str)]
		content = "final class {}Mock: {} {{\n".format(class_name, protocol_name)
		for f in funcs:
			content += "    // MARK: - {}\n".format(f.name)
			content += "    var {}_Called = false\n".format(f.name)
			if f.return_type == None:
				return_value = "()"
			elif f.return_type.endswith("?"):
				return_value = "nil"
			elif f.return_type.startswith("Driver"):
				return_value = "Driver.empty()"
			elif f.return_type.startswith("Observable"):
				return_value = "Observable.empty()"
			elif f.return_type in SWIFT_TYPES:
				return_value = SWIFT_TYPES_DEFAULT_VALUES[f.return_type]
			else:
				return_value = "{}()".format(f.return_type)
			if f.return_type != None:
				content += "    var {}_ReturnValue: {} = {}\n".format(f.name, f.return_type, return_value)
			content += "    {} {{\n".format(f.origin)
			content += "        {}_Called = true\n".format(f.name)
			if f.return_type != None:
				content += "        return {}_ReturnValue\n".format(f.name)
			content += "    }\n\n"
		content += "}\n"
		return content