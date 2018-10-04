# coding=utf-8

import re
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
			return self.type_name.endswith("]")


	def __init__(self, model_text):
		super(Model, self).__init__()
		self.model_text = model_text

	def name_and_properties(self):
		str = self.model_text
		block_regex = re.search("struct (\w+) {([^}]+)", str)
		model_name = block_regex.group(1)
		block = block_regex.group(2)
		properties_regex = re.compile("(let|var) (\w+): (.*)")
		properties = [Model.Property(p[1], p[2]) for p in properties_regex.findall(block)]
		return (model_name, properties)

class InitModel(Model):

	def create_init(self):
		model_name, properties = self.name_and_properties()
		content = "extension {} {{\n".format(model_name)

		content += "    init() {\n"
		content += "        self.init(\n"
		params = []
		for p in properties:
			if p.is_optional:
				value = "nil"
			elif p.is_array:
				value = "[]"
			elif p.type_name in SWIFT_TYPES:
				value = SWIFT_TYPES_DEFAULT_VALUES[p.type_name]
			else:
				value = "{}()".format(p.type_name)
			params.append("            {}: {}".format(p.name, value))
		content += ",\n".join(params)
		content += "\n"
		content += "        )\n"
		content += "    }\n"
		content += "}"
		return content