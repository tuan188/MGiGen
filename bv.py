# coding=utf-8
# Created by Tuan Truong on 2018-04-10.
# © 2018 Framgia.
# v1.0.0

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

def create_bind_view_model(str):
	view_model = __get_view_model_name(str)
	input_block_regex = re.compile("struct Input {([^}]+)")
	input_block = input_block_regex.search(str).group(1)
	input_properties_regex = re.compile("let (\w+): Driver<([^>]+)>")
	input_properties = [Property(p[0], p[1]) for p in input_properties_regex.findall(input_block)]
	output_block_regex = re.compile("struct Output {([^}]+)")
	output_block = output_block_regex.search(str).group(1)
	output_properties_regex = re.compile("let (\w+): Driver<([^>]+)>")
	output_properties = [Property(p[0], p[1]) for p in output_properties_regex.findall(output_block)]

	content = "    func bindViewModel() {\n"
	content += "        let input = {}ViewModel.Input(\n".format(view_model)
	args = []
	for p in input_properties:
		arg = "            {}: Driver.empty()".format(p.name)
		args.append(arg)
	content += ",\n".join(args)
	content += "\n        )\n"
	content += "        let output = viewModel.transform(input)\n"
	for p in output_properties:
		content += "        output.{}\n".format(p.name)
		content += "              .drive()\n"
		content += "              .disposed(by: rx.disposeBag)\n"
	content += "    }\n\n"
	return content

try:
	data = pasteboard_read()
	output = create_bind_view_model(data)
	pasteboard_write(output)
	print("Text has been copied to clipboard.")
except:
	print("Invalid view model text in clipboard.")
