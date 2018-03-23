# coding=utf-8
# Created by Tuan Truong on 2018-03-09.
# © 2018 Framgia.
# v1.2.0

import sys
import os
import json
from collections import namedtuple
from collections import OrderedDict
import re
import subprocess

TYPES = { 
	"int": "Int",
	"bool": "Bool",
	"unicode": "String",
	"float": "Double",
	"NoneType": "Any?"
}

DEFAULT_VALUES = {
	"Int": "0",
	"Bool": "false",
	"String": '""',
	"Double": "0.0",
	"Date": "Date()"
}

SYSTEM_TYPES = { "Int", "Bool", "String", "Double", "Date", "Any" }

DATE_REGEX = r"(\d{4})[-/](\d{2})[-/](\d{2})"

def pasteboard_read():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

def pasteboard_write(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + "".join(x.title() for x in components[1:])

def to_camel(word):
	return word[0].lower() + word[1:]

def plural_to_singular(str):
	if str.endswith("ies"):
		if len(str) > 3:
			if str[-4] not in "aeiou":
				return str[0:-3] + "y"
	elif str.endswith("es"):
		if str[-3] in "sxo":
			return str[0:-2]
		elif str[-4:-2] == "ch" or str[-4:-2] == "sh":
			return str[0:-2]
		else:
			return str[0:-1]
	elif str.endswith("s"):
		if len(str) > 3:
			return str[:-1]
	return str

class Property(object):
	def __init__(self, raw_name, name, type_name):
		self.raw_name = raw_name
		self.name = name
		self.type_name = type_name

	def is_user_type(self):
		return self.type_name.endswith("?") and self.original_type_name() not in SYSTEM_TYPES

	def is_array(self):
		return self.type_name.startswith("[")

	def original_type_name(self):
		return ''.join(c for c in self.type_name if c not in '?[]')

class Model(object):
	def __init__(self, name, properties):
		self.name = name
		self.properties = properties

	def model(self):
		content = "struct {} {{\n".format(self.name)
		for p in self.properties:
			content += "    let {}: {}\n".format(p.name, p.type_name)
		content += "}\n\n"
		return content

	def builder(self):
		content = "final class {}Builder: Then {{\n".format(self.name)
		for p in self.properties:
			if p.type_name.endswith("?"):
				if p.original_type_name() in SYSTEM_TYPES:
					content += "    var {}: {}\n".format(p.name, p.type_name)
				else:
					if not p.is_array():
						content += "    var {}: {}Builder?\n".format(p.name, p.original_type_name())
					else:
						content += "    var {}: [{}Builder]?\n".format(p.name, p.original_type_name())
			else:
				if p.type_name in DEFAULT_VALUES:
					default_value = DEFAULT_VALUES[p.type_name]
				else:
					default_value = "{}()".format(p.type_name)
				content += "    var {}: {} = {}\n".format(p.name, p.type_name, default_value)
		
		content += "\n"
		content += "    init() {\n\n    }\n\n"
		lower_name = to_camel(self.name)
		content += "    init({}: {}) {{\n".format(lower_name, self.name)
		for p in self.properties:
			if not p.is_user_type():
				content += "        {} = {}.{}\n".format(p.name, lower_name, p.name)
			else:
				if not p.is_array():	
					content += "        {} = {}.{}.map {{ {}Builder({}: $0) }}\n".format(
						p.name, lower_name, p.name, p.original_type_name(), to_camel(p.name)) 
				else:
					content += "        {} = {}.{}.map {{ $0.map {{ {}Builder({}: $0) }} }}\n".format(
						p.name, lower_name, p.name, p.original_type_name(), plural_to_singular(to_camel(p.name))) 
		content += "    }\n}\n\n"
		# ObjectMapper
		content += "extension {}Builder: Mappable {{\n".format(self.name)
		content += "    convenience init?(map: Map) {\n        self.init()\n    }\n\n"
		content += "    func mapping(map: Map) {\n"
		for p in self.properties:
			if not p.original_type_name() == "Date":
				content += '        {} <- map["{}"]\n'.format(p.name, p.raw_name)
			else:
				content += '        {} <- (map["{}"], DateTransform())\n'.format(p.name, p.raw_name)
		content += "    }\n}\n\n"
		# Init
		content += "extension {} {{\n".format(self.name)
		content += "    init(builder: {}Builder) {{\n".format(self.name)
		content += "        self.init(\n"
		args = []
		for p in self.properties:
			if not p.is_user_type():
				arg = "            {}: builder.{}".format(p.name, p.name)
			elif p.is_array():
				arg = "            {}: builder.{}.map {{ $0.map {{ {}(builder: $0) }} }}".format(
					p.name, p.name, p.original_type_name())
			else:
				arg = "            {}: builder.{}.map {{ {}(builder: $0) }}".format(
					p.name, p.name, p.original_type_name())
			args.append(arg)
		content += ",\n".join(args)
		content += "\n        )\n    }\n\n"
		content += "    init() {\n"
		content += "        self.init(builder: {}Builder())\n".format(self.name)
		content += "    }\n}\n\n"
		return content

	def toString(self):
		return "".join([self.model(), self.builder()])

def extract_model(name, dictionary, models):
	properties = []
	for key in dictionary.keys():
		var_name = snake_to_camel(key)
		value = dictionary[key]
		type_name = type(value).__name__
		if type_name == "OrderedDict":
			var_type = var_name.title() + "?"
			extract_model(var_name.title(), value, models)
		elif type_name == "list":
			singular_var_name = plural_to_singular(var_name)
			var_type = "[{}]?".format(singular_var_name.title())
			if len(value) > 0:
				extract_model(singular_var_name.title(), value[0], models)
			else:
				var_type = "[Any]?"
		else:
			var_type = TYPES[type_name]
			if var_type == "String":
				if re.match(DATE_REGEX, value):
					var_type = "Date"
			if var_type == "Any?":
				if var_name.endswith("Url") \
					or "name" in var_name.lower() \
					or "email" in var_name.lower() \
					or var_name.endswith("Key") \
					or var_name.endswith("Token"):
					var_type = "String?"
				elif "time" in var_name.lower() \
					or "date" in var_name.lower() \
					or var_name.endswith("At") \
					or "birthday" in var_name.lower():
					var_type = "Date?"
				elif var_name.endswith("Id"):
					var_type = "Int?"
		property = Property(key, var_name, var_type)
		properties.append(property)
	model = Model(name, properties)
	models.append(model)

try:
	if len(sys.argv) > 1:
		model_name = sys.argv[1]
	else:
		model_name = raw_input('Enter a model name: ')
	data = pasteboard_read()
	dictionary = json.loads(data, object_pairs_hook=OrderedDict)
	modelList = []
	extract_model(model_name, dictionary, modelList)
	output = "import ObjectMapper\nimport Then\n\n"
	output += "".join([model.toString() for model in modelList])

	file_name = model_name + ".swift"
	with open(file_name, "w") as f:
		f.write(output)
	print("{} has been created.".format(file_name))
	pasteboard_write(output)
	print("Text has been copied to clipboard.")
except:
	print("Invalid json string in clipboard.")



