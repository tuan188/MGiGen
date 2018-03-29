# coding=utf-8
# Created by Tuan Truong on 2018-03-26.
# © 2018 Framgia.
# v1.0.1

import sys
import os
import re
import subprocess

def pasteboard_read():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

def pasteboard_write(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

class Property(object):
	def __init__(self, name, type_name):
		super(Property, self).__init__()
		self.name = name
		self.type_name = type_name

	def __str__(self):
		return "let {}: Driver<{}>".format(self.name, self.type_name)

	def builder_property(self):
		return "var {}: Driver<{}> = Driver.empty()".format(self.name, self.type_name)


def __get_view_model_name(str):
	regex = re.compile("struct (.+)ViewModel:")
	mo = regex.search(str)
	return mo.group(1)

def create_builder(str):
	input_block_regex = re.compile("struct Input {([^}]+)")
	input_block = input_block_regex.search(str).group(1)
	properties_regex = re.compile("let (\w+): Driver<([^>]+)>")
	properties = [Property(p[0], p[1]) for p in properties_regex.findall(input_block)]
	view_model = __get_view_model_name(str)
	content = "\nextension {}ViewModel {{\n".format(view_model)
	content += "    final class InputBuilder: Then {\n"
	for p in properties:
		content += "       {}\n".format(p.builder_property())
	content += "    }\n}\n\n"
	content += "extension {}ViewModel.Input {{\n".format(view_model)
	content += "    init(builder: {}ViewModel.InputBuilder) {{\n".format(view_model)
	content += "        self.init(\n"
	args = []
	for p in properties:
		arg = "            {}: builder.{}".format(p.name, p.name)
		args.append(arg)
	content += ",\n".join(args)
	content += "\n        )\n    }\n}\n"
	return content

try:
	data = pasteboard_read()
	output = create_builder(data)
	pasteboard_write(output)
	print("Text has been copied to clipboard.")
except:
	print("Invalid view model text in clipboard.")



