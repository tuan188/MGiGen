# coding=utf-8

import json
import re
from collections import OrderedDict
from jinja2 import Environment, PackageLoader
from .pb import pasteboard_write
from .constants import SWIFT_TYPES_DEFAULT_VALUES, SWIFT_TYPES
from .str_helpers import snake_to_camel, plural_to_singular
from .command import Command

class JSONCommand(Command):
	def __init__(self, model_name, json_text):
		super(JSONCommand, self).__init__()
		self.model_name = model_name
		self.json_text = json_text

	def create_models(self, print_result):
		output = JSON(self.model_name, self.json_text).create_models()
		if print_result:
			print()
			print(output)
			print()
		pasteboard_write(output)
		print('The result has been copied to the pasteboard.')


class JSON(object):

	JSON_TO_SWIFT_TYPES = { 
		"int": "Int",
		"bool": "Bool",
		"str": "String",
		"float": "Double",
		"NoneType": "Any?"
	}

	DATE_REGEX = r"(\d{4})[-/](\d{2})[-/](\d{2})"

	class Property(object):
		def __init__(self, raw_name, name, type_name):
			self.raw_name = raw_name
			self.name = name
			self.type_name = type_name

		@property
		def is_user_type(self):
			return self.is_optional and self.original_type_name() not in SWIFT_TYPES

		@property
		def is_optional(self):
			return self.type_name.endswith("?")

		@property
		def is_array(self):
			return self.type_name.startswith("[")

		@property
		def is_date(self):
			return self.original_type_name == "Date"

		@property
		def original_type_name(self):
			return ''.join(c for c in self.type_name if c not in '?[]')

		@property
		def value(self):
			if self.is_optional:
				value = "nil"
			elif self.is_array:
				value = "[]"
			elif self.type_name in SWIFT_TYPES_DEFAULT_VALUES:
				value = SWIFT_TYPES_DEFAULT_VALUES[self.type_name]
			else:
				value = "{}()".format(self.type_name)
			return value

	class Model(object):
		def __init__(self, name, properties):
			self.name = name
			self.properties = properties

		def model(self):
			env = Environment(
				loader=PackageLoader('igen_templates', 'commands'),
				trim_blocks=True,
				lstrip_blocks=True
			)
			template = env.get_template("JSON.swift")
			content = template.render(
				name=self.name,
				properties=self.properties
			)
			return content

		def __str__(self):
			return self.model()

	def __init__(self, model_name, json_text):
		self.model_name = model_name
		self.json_text = json_text

	def create_models(self):
		try:
			dictionary = json.loads(self.json_text, object_pairs_hook=OrderedDict)
			models = []
			self._extract_model(self.model_name, dictionary, models)
			output = "\n\n".join([model.__str__() for model in models])
			return output
		except:
			print("The JSON in the pasteboard is invalid.")
			exit(1)

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
