# coding=utf-8
# Created by Tuan Truong on 2018-04-10.
# © 2018 Framgia.
# v1.0.1

import sys
import os
import re
import subprocess

def pasteboard_read():
	return subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

def pasteboard_write(output):
	process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
	process.communicate(output.encode('utf-8'))

DEFAULT_VALUES = {
	"Int": "0",
	"Bool": "false",
	"String": '""',
	"Double": "0.0",
	"Float": "0.0",
	"Date": "Date()"
}

SYSTEM_TYPES = { "Int", "Bool", "String", "Double", "Float", "Date" }

class Function(object):
	def __init__(self, origin, name, return_type):
		super(Function, self).__init__()
		self.origin = origin
		self.name = name
		self.return_type = return_type

	def __str__(self):
		return self.origin
		# return "let {}: {}".format(self.name, self.return_type)

def __get_protocol_name(str):
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

def create_mock(str):
	(protocol_name, class_name) = __get_protocol_name(str)
	func_regex = re.compile("func (\w+)\(.*\)( -> (.*))?")
	funcs = [Function(f.group(), f.group(1), f.group(3)) for f in func_regex.finditer(str)]
	content = "final class {}Mock: {} {{\n\n".format(class_name, protocol_name)
	for f in funcs:
		content += "    // MARK: - {}\n\n".format(f.name)
		content += "    var {}_Called = false\n".format(f.name)
		if f.return_type == None:
			return_value = "()"
		elif f.return_type.endswith("?"):
			return_value = "nil"
		elif f.return_type.startswith("Driver"):
			return_value = "Driver.empty()"
		elif f.return_type.startswith("Observable"):
			return_value = "Observable.empty()"
		elif f.return_type in SYSTEM_TYPES:
			return_value = DEFAULT_VALUES[f.return_type]
		else:
			return_value = "{}()".format(f.return_type)
		if f.return_type != None:
			content += "    var {}_ReturnValue: {} = {}\n\n".format(f.name, f.return_type, return_value)
		content += "    {} {{\n".format(f.origin)
		content += "        {}_Called = true\n".format(f.name)
		if f.return_type != None:
			content += "        return {}_ReturnValue\n".format(f.name)
		content += "    }\n\n"
	content += "}\n"
	return content

try:
	data = pasteboard_read()
	output = create_mock(data)
	pasteboard_write(output)
	print("Text has been copied to clipboard.")
except:
	print("Invalid view model text in clipboard.")
