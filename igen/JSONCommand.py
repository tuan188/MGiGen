# coding=utf-8

import json
import re
from collections import OrderedDict
from Pasteboard import pasteboard_write
from Constants import SWIFT_TYPES_DEFAULT_VALUES, SWIFT_TYPES
from StringHelpers import snake_to_camel, plural_to_singular
from Command import Command

class JSONCommand(Command):
	def __init__(self, model_name, json_text):
		super(JSONCommand, self).__init__()
		self.model_name = model_name
		self.json_text = json_text

	@classmethod
	def description(cls):
		return "Create models from json text"

	@classmethod
	def name(cls):
		return "json"

	def create_models(self):
		# try:
		output = JSON(self.model_name, self.json_text).create_models()
		pasteboard_write(output)
		print("Text has been copied to clipboard.")
		# except:
		# 	print("Invalid json string in clipboard


class JSON(object):

	JSON_TO_SWIFT_TYPES = { 
		"int": "Int",
		"bool": "Bool",
		"unicode": "String",
		"float": "Double",
		"NoneType": "Any?"
	}

	DATE_REGEX = r"(\d{4})[-/](\d{2})[-/](\d{2})"

	class Property(object):
		def __init__(self, raw_name, name, type_name):
			self.raw_name = raw_name
			self.name = name
			self.type_name = type_name

		def is_user_type(self):
			return self.type_name.endswith("?") and self.original_type_name() not in SWIFT_TYPES

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
				content += "    var {}: {}\n".format(p.name, p.type_name)
			content += "}\n\n"
			content += "extension {} {{\n".format(self.name)
			content += "    init() {\n"
			content += "        self.init(\n"
			params = []
			for p in self.properties:
				if p.type_name.endswith("?"):
					params.append("            {}: nil".format(p.name))
				elif p.type_name.endswith("]"):
					params.append("            {}: []".format(p.name))
				else:
					if p.type_name in SWIFT_TYPES_DEFAULT_VALUES:
						default_value = SWIFT_TYPES_DEFAULT_VALUES[p.type_name]
					else:
						default_value = "{}()".format(p.type_name)
					params.append("            {}: {}".format(p.name, default_value))
			content += ",\n".join(params)
			content += "\n"
			content += "        )\n"
			content += "    }\n"
			content += "}\n\n"
			content += "extension {}: Then {{ }}\n\n".format(self.name)
			content += "extension {}: Mappable {{\n".format(self.name)
			content += "    init?(map: Map) {\n"
			content += "        self.init()\n"
			content += "    }\n\n"
			content += "    mutating func mapping(map: Map) {\n"
			for p in self.properties:
				if not p.original_type_name() == "Date":
					content += '        {} <- map["{}"]\n'.format(p.name, p.raw_name)
				else:
					content += '        {} <- (map["{}"], DateTransform())\n'.format(p.name, p.raw_name)
			content += "    }\n"
			content += "}\n\n"
			return content

		def __str__(self):
			return self.model()

	def __init__(self, model_name, json_text):
		self.model_name = model_name
		self.json_text = json_text

	def create_models(self):
		dictionary = json.loads(self.json_text, object_pairs_hook=OrderedDict)
		models = []
		self._extract_model(self.model_name, dictionary, models)
		output = "import ObjectMapper\nimport Then\n\n"
		output += "".join([model.__str__() for model in models])
		return output


	def _extract_model(self, name, dictionary, models):
		properties = []
		for key in dictionary.keys():
			var_name = snake_to_camel(key)
			value = dictionary[key]
			type_name = type(value).__name__
			if type_name == "OrderedDict":
				var_type = var_name.title() + "?"
				self._extract_model(var_name.title(), value, models)
			elif type_name == "list":
				singular_var_name = plural_to_singular(var_name)
				var_type = "[{}]".format(singular_var_name.title())
				if len(value) > 0:
					self._extract_model(singular_var_name.title(), value[0], models)
				else:
					var_type = "[Any]"
			else:
				var_type = JSON.JSON_TO_SWIFT_TYPES[type_name]
				if var_type == "String":
					if re.match(JSON.DATE_REGEX, value):
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
			property = JSON.Property(key, var_name, var_type)
			properties.append(property)
		model = JSON.Model(name, properties)
		models.append(model)
