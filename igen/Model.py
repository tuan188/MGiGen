# coding=utf-8

import re
from jinja2 import Environment, PackageLoader
from .constants import SWIFT_TYPES_DEFAULT_VALUES, SWIFT_TYPES

class Model(object):

	class Property(object):
		def __init__(self, name, type_name):
			super(Model.Property, self).__init__()
			self.name = name
			self.type_name = type_name

		@property
		def is_optional(self):
			return self.type_name.endswith("?")

		@property
		def is_array(self):
			return self.type_name.endswith("]") and ':' not in self.type_name

		@property
		def is_dictionary(self):
			return self.type_name.endswith("]") and ':' in self.type_name

		@property
		def is_observable(self):
			return self.type_name.startswith('Observable')
		
		@property
		def is_driver(self):
			return self.type_name.startswith('Driver')

		@property
		def value(self):
			if self.is_optional:
				value = "nil"
			elif self.is_array:
				value = "[]"
			elif self.is_dictionary:
				value = "[:]"
			elif self.type_name in SWIFT_TYPES:
				value = SWIFT_TYPES_DEFAULT_VALUES[self.type_name]
			elif self.is_observable:
				value = 'Observable.empty()'
			elif self.is_driver:
				value = 'Driver.empty()'
			else:
				value = "{}()".format(self.type_name)
			return value


	def __init__(self, model_text):
		super(Model, self).__init__()
		self.model_text = model_text

	def name_and_properties(self):
		try:
			str = self.model_text
			block_regex = re.search("(?:struct|class) (\w+) {([^}]+)", str)
			model_name = block_regex.group(1)
			block = block_regex.group(2)
			properties_regex = re.compile("(let|var) (\w+): (.*)")
			properties = [Model.Property(p[1], p[2]) for p in properties_regex.findall(block)]
			return (model_name, properties)
		except:
			print("The model in the pasteboard is invalid.")
			exit(1)
		

class InitModel(Model):

	def create_init(self):
		model_name, properties = self.name_and_properties()
		env = Environment(
			loader=PackageLoader('igen_templates', 'commands'),
			trim_blocks=True,
			lstrip_blocks=True
		)
		template = env.get_template("Init.swift")
		content = template.render(
			name=model_name,
			properties=properties
		)
		return content
