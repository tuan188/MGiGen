# coding=utf-8

import sys
import os
from datetime import datetime
import subprocess
import re
from collections import OrderedDict
import json
from jinja2 import Environment, PackageLoader

#=================== Helpers ===================

def pasteboard_read():
	return subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

def pasteboard_write(output):
	process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
	process.communicate(output.encode('utf-8'))

def lower_first_letter(st):
	return st[0].lower() + st[1:]

def upper_first_letter(st):
	return st[0].upper() + st[1:]

def snake_to_camel(st):
    components = st.split('_')
    return components[0] + "".join(x.title() for x in components[1:])

def plural_to_singular(st):
	if st.endswith("ies"):
		if len(st) > 3:
			if st[-4] not in "aeiou":
				return st[0:-3] + "y"
	elif st.endswith("es"):
		if st[-3] in "sxo":
			return st[0:-2]
		elif st[-4:-2] == "ch" or st[-4:-2] == "sh":
			return st[0:-2]
		else:
			return st[0:-1]
	elif st.endswith("s"):
		if len(st) > 3:
			return st[:-1]
	return st


#=================== Constants ===================

FILE_HEADER = "file_header.txt"

SWIFT_TYPES_DEFAULT_VALUES = {
	"Int": "0",
	"Bool": "false",
	"String": '""',
	"Double": "0.0",
	"Float": "0.0",
	"Date": "Date()"
}

SWIFT_TYPES = { 
	"Int", 
	"Bool", 
	"String", 
	"Double", 
	"Float"
	"Date"
}


#=================== BaseTemplate ===================

class Template(object):

	class Model(object):
		def __init__(self, name, properties):
			super(Template.Model, self).__init__()
			self.name = name
			self.properties = properties


	class Property(object):
		def __init__(self, property):
			super(Template.Property, self).__init__()
			self.property = property
			property_regex = re.compile("(?:let|var) (\w+): (.*)")
			mo = property_regex.search(property)
			self.name = mo.group(1)
			self.name_title = upper_first_letter(self.name)
			self.type = Template.PropertyType(mo.group(2))

		@property
		def is_url(self):
			lowered_name = self.name.lower()
			if lowered_name.endswith("id"):
				return False
			return "image" in lowered_name or "url" in lowered_name
		

	class PropertyType(object):
		def __init__(self, name):
			super(Template.PropertyType, self).__init__()
			self.name = name

		def is_optional(self):
			return self.name.endswith("?")

		def is_array(self):
			return self.name.endswith(("]", "]?"))

	class TemplateType:
		BASE = "-base"
		LIST = "-list"
		DETAIL = "-detail"

	def parse_model(self, model_text):
		model_regex = re.compile("(?:struct|class) (\w+) {((.|\n)*)}")
		match = model_regex.search(model_text)
		model_name = match.group(1)
		property_block = match.group(2)
		property_regex = re.compile("(?:let|var) (\w+): (.*)")
		properties = [Template.Property(p.group()) for p in property_regex.finditer(property_block)]
		return Template.Model(model_name, properties)

	class BaseTemplate(object):
		def __init__(self, name, project, developer, company, date):
			super(Template.BaseTemplate, self).__init__()
			self.name = name
			self.project = project
			self.developer = developer
			self.company = company
			self.date = date
			self.env = Environment(
				loader=PackageLoader('igen_templates', 'base'),
				trim_blocks=True,
				lstrip_blocks=True
			)

		def _create_file(self, class_name, content):
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self.__create_file(file_path, file_name, content)

		def _create_test_file(self, class_name, content):
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self.__create_file(file_path, file_name, content)

		def __create_file(self, file_path, file_name, content):
			with open(file_path, "w") as f:
				f.write(content.encode('utf8'))
				print("        new file:   {}".format(file_path))

		def _file_header(self, class_name):
			template = self.env.get_template("header.swift")
			header = template.render(
				class_name=class_name,
				project=self.project,
				developer=self.developer,
				created_date=self.date,
				copyright_year=datetime.now().year,
				company=self.company
			)
			return header + "\n\n"

		def create_files(self):
			print(" ")
			self._make_dirs()
			self._create_view_model()
			self._create_navigator()
			self._create_use_case()
			self._create_view_controller()
			self._create_assembler()
			# Test
			self._create_view_model_tests()
			self._create_use_case_mock()
			self._create_navigator_mock()
			self._create_view_controller_tests()
			print(" ")

		def _make_dirs(self):
			current_directory = os.getcwd()
			main_directory = os.path.join(current_directory, r'{}'.format(self.name))
			try: 
				os.makedirs(main_directory)
			except:
				pass
			test_directory = os.path.join(main_directory, "Test")
			try:
				os.makedirs(test_directory)
			except:
				pass

		def _create_view_model(self):
			class_name = self.name + "ViewModel"
			template = self.env.get_template("ViewModel.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name
			)
			self._create_file(class_name, content)

		def _create_navigator(self):
			class_name = self.name + "Navigator"
			template = self.env.get_template("Navigator.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name
			)
			self._create_file(class_name, content)

		def _create_use_case(self):
			class_name = self.name + "UseCase"
			template = self.env.get_template("UseCase.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name
			)
			self._create_file(class_name, content)

		def _create_view_controller(self):
			class_name = self.name + "ViewController"
			template = self.env.get_template("ViewController.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name
			)
			self._create_file(class_name, content)

		def _create_assembler(self):
			class_name = self.name + "Assembler"
			template = self.env.get_template("Assembler.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name
			)
			self._create_file(class_name, content)

		def _create_view_model_tests(self):
			class_name = self.name + "ViewModelTests"
			template = self.env.get_template("ViewModelTests.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				project=self.project
			)
			self._create_test_file(class_name, content)

		def _create_use_case_mock(self):
			class_name = self.name + "UseCaseMock"
			template = self.env.get_template("UseCaseMock.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				project=self.project
			)
			self._create_test_file(class_name, content)

		def _create_navigator_mock(self):
			class_name = self.name + "NavigatorMock"
			template = self.env.get_template("NavigatorMock.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				project=self.project
			)
			self._create_test_file(class_name, content)

		def _create_view_controller_tests(self):
			class_name = self.name + "ViewControllerTests"
			template = self.env.get_template("ViewControllerTests.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				project=self.project
			)
			self._create_test_file(class_name, content)



	#=================== ListTemplate ===================

	class ListTemplate(BaseTemplate):

		def __init__(self, model, options, name, project, developer, company, date):
			super(Template.ListTemplate, self).__init__(name, project, developer, company, date)
			self.model = model
			self.options = options
			self.is_sectioned_list = "--section" in options
			self.is_collection = "--collection" in options
			self.model_name = self.model.name
			self.model_variable = lower_first_letter(self.model_name)
			self.env = Environment(
				loader=PackageLoader('igen_templates', 'list'),
				trim_blocks=True,
				lstrip_blocks=True
			)

		def create_files(self):
			print(" ")
			self._make_dirs()
			self._create_view_model()
			self._create_item_view_model()
			self._create_navigator()
			self._create_use_case()
			self._create_view_controller()
			self._create_table_view_cell()
			self._create_assembler()
			# Test
			self._create_view_model_tests()
			self._create_use_case_mock()
			self._create_navigator_mock()
			self._create_view_controller_tests()
			self._create_table_view_cell_tests()
			print(" ")

		def _create_view_model(self):
			class_name = self.name + "ViewModel"
			if self.is_sectioned_list:
				template_name = "SectionedViewModel.swift"
			else:
				template_name = "ViewModel.swift"
			template = self.env.get_template(template_name)
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				model_name=self.model_name,
				model_variable=self.model_variable
			)
			self._create_file(class_name, content)

		def _create_item_view_model(self):
			class_name = self.model_name + "ViewModel"
			template = self.env.get_template("ItemViewModel.swift")
			content = self._file_header(class_name)
			content += template.render(
				model_name=self.model_name,
				model_variable=self.model_variable,
				properties=self.model.properties
			)
			self._create_file(class_name, content)

		def _create_use_case(self):
			class_name = self.name + "UseCase"
			template = self.env.get_template("UseCase.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				model_name=self.model_name
			)
			self._create_file(class_name, content)

		def _create_navigator(self):
			class_name = self.name + "Navigator"
			template = self.env.get_template("Navigator.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				model_name=self.model_name,
				model_variable=self.model_variable
			)
			self._create_file(class_name, content)

		def _create_view_controller(self):
			class_name = self.name + "ViewController"
			if self.is_sectioned_list:
				if self.is_collection:
					template_file = "SectionedCollectionViewController.swift"
				else:
					template_file = "SectionedTableViewController.swift"
			else:
				if self.is_collection:
					template_file = "CollectionViewController.swift"
				else:
					template_file = "TableViewController.swift"
			template = self.env.get_template(template_file)
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				model_name=self.model_name,
				model_variable=self.model_variable
			)
			self._create_file(class_name, content)

		def _create_table_view_cell(self):
			class_name = self.model_name + "Cell"
			if self.is_collection:
				template_file = "CollectionViewCell.swift"
			else:
				template_file = "TableViewCell.swift"
			template = self.env.get_template(template_file)
			content = self._file_header(class_name)
			content += template.render(
				model_name=self.model_name,
				model_variable=self.model_variable,
				properties=self.model.properties
			)
			self._create_file(class_name, content)

		def _create_view_model_tests(self):
			class_name = self.name + "ViewModelTests"
			if self.is_sectioned_list:
				template_name = "SectionedViewModelTests.swift"
			else:
				template_name = "ViewModelTests.swift"
			template = self.env.get_template(template_name)
			content = self._file_header(class_name)
			content += template.render(
				project=self.project,
				name=self.name,
				model_name=self.model_name,
				model_variable=self.model_variable
			)
			self._create_test_file(class_name, content)

		def _create_use_case_mock(self):
			class_name = self.name + "UseCaseMock"
			template = self.env.get_template("UseCaseMock.swift")
			content = self._file_header(class_name)
			content += template.render(
				project=self.project,
				name=self.name,
				model_name=self.model_name
			)
			self._create_test_file(class_name, content)

		def _create_navigator_mock(self):
			class_name = self.name + "NavigatorMock"
			template = self.env.get_template("NavigatorMock.swift")
			content = self._file_header(class_name)
			content += template.render(
				project=self.project,
				name=self.name,
				model_name=self.model_name,
				model_variable=self.model_variable
			)
			self._create_test_file(class_name, content)

		def _create_view_controller_tests(self):
			class_name = self.name + "ViewControllerTests"
			if self.is_collection:
				template_name = "CollectionViewControllerTests.swift"
			else:
				template_name = "TableViewControllerTests.swift"
			template = self.env.get_template(template_name)
			content = self._file_header(class_name)
			content += template.render(
				project=self.project,
				name=self.name
			)
			self._create_test_file(class_name, content)

		def _create_table_view_cell_tests(self):
			class_name = "{}CellTests".format(self.model_name)
			template_name = "TableViewCellTests.swift"
			template = self.env.get_template(template_name)
			content = self._file_header(class_name)
			content += template.render(
				project=self.project,
				model_name=self.model_name,
				properties=self.model.properties
			)
			self._create_test_file(class_name, content)


	#=================== DetailTemplate ===================


	class DetailTemplate(BaseTemplate):
		def __init__(self, model, options, name, project, developer, company, date):
			super(Template.DetailTemplate, self).__init__(name, project, developer, company, date)
			self.model = model
			self.options = options
			self.model_name = self.model.name
			self.model_variable = lower_first_letter(self.model_name)
			self.env = Environment(
				loader=PackageLoader('igen_templates', 'detail'),
				trim_blocks=True,
				lstrip_blocks=True
			)

		def create_files(self):
			print(" ")
			self._make_dirs()
			self._create_view_model()
			self._create_navigator()
			self._create_use_case()
			self._create_view_controller()
			self._create_cells()
			self._create_assembler()
			# Test
			self._create_view_model_tests()
			self._create_use_case_mock()
			self._create_navigator_mock()
			self._create_view_controller_tests()
			self._create_cells_tests()
			print(" ")

		def _create_view_model(self):
			class_name = self.name + "ViewModel"
			template = self.env.get_template("ViewModel.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				model_name=self.model_name,
				model_variable=self.model_variable,
				properties=self.model.properties
			)
			self._create_file(class_name, content)

		def _create_view_controller(self):
			class_name = self.name + "ViewController"
			template = self.env.get_template("ViewController.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				model_name=self.model_name,
				properties=self.model.properties
			)
			self._create_file(class_name, content)

		def _create_cells(self):
			for p in self.model.properties:
				self._create_cell(p)

		def _create_cell(self, property):
			class_name = "{}{}Cell".format(self.model_name, property.name_title)
			template = self.env.get_template("Cell.swift")
			content = self._file_header(class_name)
			content += template.render(
				model_name=self.model_name,
				property_name=property.name,
				property_name_title=property.name_title
			)
			self._create_file(class_name, content)

		def _create_view_model_tests(self):
			class_name = self.name + "ViewModelTests"
			template = self.env.get_template("ViewModelTests.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				project=self.project,
				model_name=self.model_name,
				model_variable=self.model_variable
			)
			self._create_test_file(class_name, content)

		def _create_view_controller_tests(self):
			class_name = self.name + "ViewControllerTests"
			template = self.env.get_template("ViewControllerTests.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				project=self.project,
			)
			self._create_test_file(class_name, content)

		def _create_cells_tests(self):
			class_name = "{}CellsTests".format(self.name)
			template = self.env.get_template("CellsTests.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				project=self.project,
				model_name=self.model_name,
				model_variable=self.model_variable,
				properties=self.model.properties
			)
			self._create_test_file(class_name, content)


	#=================== StaticDetailTemplate ===================


	class StaticDetailTemplate(DetailTemplate):

		def create_files(self):
			print(" ")
			self._make_dirs()
			self._create_assembler()
			self._create_view_model()
			self._create_navigator()
			self._create_use_case()
			self._create_view_controller()
			self._create_view_model_tests()
			self._create_use_case_mock()
			self._create_navigator_mock()
			self._create_view_controller_tests()
			print(" ")

		def _create_view_model(self):
			class_name = self.name + "ViewModel"
			template = self.env.get_template("StaticViewModel.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				model_name=self.model_name,
				model_variable=self.model_variable,
				properties=self.model.properties
			)
			self._create_file(class_name, content)

		def _create_view_controller(self):
			class_name = self.name + "ViewController"
			template = self.env.get_template("StaticViewController.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				properties=self.model.properties
			)
			self._create_file(class_name, content)

		def _create_view_model_tests(self):
			class_name = self.name + "ViewModelTests"
			template = self.env.get_template("StaticViewModelTests.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				project=self.project,
				model_name=self.model_name,
				model_variable=self.model_variable,
				properties=self.model.properties
			)
			self._create_test_file(class_name, content)

		def _create_view_controller_tests(self):
			class_name = self.name + "ViewControllerTests"
			template = self.env.get_template("StaticViewControllerTests.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				project=self.project,
				properties=self.model.properties
			)
			self._create_test_file(class_name, content)

#=================== JSON ===================


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

#=================== Mock ===================


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

#=================== API ===================

class API(object):
	def __init__(self, api_name):
		super(API, self).__init__()
		self.api_name = api_name

	def create_api(self):
		name = self.api_name
		var_name = lower_first_letter(name)
		content = "// MARK: - {}\n".format(name)
		content += "extension API {\n"
		content += "    func {}(_ input: {}Input) -> Observable<{}Output> {{\n".format(var_name, name, name)
		content += "        return request(input)\n"
		content += "    }\n\n"
		content += "    final class {}Input: APIInput {{\n".format(name)
		content += "        init() {\n"
		content += "            super.init(urlString: API.Urls.{},\n".format(var_name)
		content += "                       parameters: nil,\n"
		content += "                       requestType: .get,\n"
		content += "                       requireAccessToken: true)\n"
		content += "        }\n    }\n\n"
		content += "    final class {}Output: APIOutput {{\n".format(name)
		content += "        override func mapping(map: Map) {\n"
		content += "            super.mapping(map: map)\n"
		content += "        }\n    }\n}\n"
		return content

#=================== ViewModel ===================

class ViewModel(object):

	class Property(object):
		def __init__(self, name, type_name):
			super(ViewModel.Property, self).__init__()
			self.name = name
			self.type_name = type_name

		def __str__(self):
			return "let {}: Driver<{}>".format(self.name, self.type_name)

	def __init__(self, vm_text):
		super(ViewModel, self).__init__()
		self.vm_text = vm_text

	@property
	def view_model_name(self):
		regex = re.compile("(?:struct|extension) (\w+)ViewModel")
		mo = regex.search(self.vm_text)
		return mo.group(1)

	@property
	def properties(self):
		str = self.vm_text
		input_block_regex = re.compile("struct Input {([^}]+)")
		input_block = input_block_regex.search(str).group(1)
		input_properties_regex = re.compile("let (\w+): Driver<([^>]+)>")
		input_properties = [ViewModel.Property(p[0], p[1]) for p in input_properties_regex.findall(input_block)]
		output_block_regex = re.compile("struct Output {([^}]+)")
		output_block = output_block_regex.search(str).group(1)
		output_properties_regex = re.compile("let (\w+): Driver<([^>]+)>")
		output_properties = [ViewModel.Property(p[0], p[1]) for p in output_properties_regex.findall(output_block)]
		return (input_properties, output_properties)
	

class UnitTest(ViewModel):

	def create_tests(self):
		view_model = self.view_model_name
		input_properties, output_properties = self.properties
		content = "final class {}ViewModelTests: XCTestCase {{\n".format(view_model)
		content += "    private var viewModel: {}ViewModel!\n".format(view_model)
		content += "    private var navigator: {}NavigatorMock!\n".format(view_model)
		content += "    private var useCase: {}UseCaseMock!\n".format(view_model)
		content += "    private var disposeBag: DisposeBag!\n"
		content += "    private var input: {}ViewModel.Input!\n".format(view_model)
		content += "    private var output: {}ViewModel.Output!\n".format(view_model)
		for p in input_properties:
			content += "    private let {} = PublishSubject<{}>()\n".format(p.name, p.type_name)
		content += "\n"
		content += "    override func setUp() {\n"
		content += "        super.setUp()\n"
		content += "        navigator = {}NavigatorMock()\n".format(view_model)
		content += "        useCase = {}UseCaseMock()\n".format(view_model)
		content += "        viewModel = {}ViewModel(navigator: navigator, useCase: useCase)\n".format(view_model)
		content += "        disposeBag = DisposeBag()\n\n"
		content += "        input = {}ViewModel.Input(\n".format(view_model)
		args = []
		for p in input_properties:
			arg = "            {}: {}.asDriverOnErrorJustComplete()".format(p.name, p.name)
			args.append(arg)
		content += ",\n".join(args)
		content += "\n        )\n"
		content += "        output = viewModel.transform(input)\n"
		for p in output_properties:
			content += "        output.{}.drive().disposed(by: disposeBag)\n".format(p.name)
		content += "    }\n\n"
		for p in input_properties:
			content += "    func test_{}_() {{\n".format(p.name)
			content += "        // arrange\n\n\n"
			content += "        // act\n\n\n"
			content += "        // assert\n"
			content += "        XCTAssert(true)\n"
			content += "    }\n\n"
		content += "}\n"
		return content
		
class BindViewModel(ViewModel):

	def create_bind_view_model(self):
		view_model = self.view_model_name
		input_properties, output_properties = self.properties

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
		

#=================== Model ===================


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


#=================== Commands ===================

class Commands:
	HELP = "help"
	HEADER = "header"
	TEMPLATE = "template"
	JSON = "json"
	MOCK = "mock"
	API = "api"
	UNIT_TEST = "test"
	BIND_VIEW_MODEL = "bind"
	INIT = "init"

class HelpCommand(object):
	def __init__(self):
		super(HelpCommand, self).__init__()
		
	def show_help(self):
		help = "igen commands:\n"
		help += format("   help", "<15") + "Show help\n"
		help += format("   header", "<15") + "Update file header info\n"
		help += format("   template", "<15") + "Generate template files\n"
		help += format("   json", "<15") + "Create models from json text\n"
		help += format("   mock", "<15") + "Create mock from protocol\n"
		help += format("   api", "<15") + "Create API request\n"
		help += format("   test", "<15") + "Create Unit Tests from view model\n"
		help += format("   bind", "<15") + "Create bindViewModel method for view controller from view model\n"
		help += format("   init", "<15") + "Create init method for struct model\n"
		help += "\n"
		help += "Get help on a command: igen help [command]\n"
		print(help)


class FileHeaderCommand(object):
	def __init__(self):
		super(FileHeaderCommand, self).__init__()

	def update_file_header(self):
		project = raw_input('Enter project name: ')
		developer = raw_input('Enter developer name: ')
		company = raw_input('Enter company name: ')
		content = "\n".join([project, developer, company])
		with open(FILE_HEADER, "w") as f:	
			f.write(content)
		return (project, developer, company)


class TemplateCommmand(object):
	def __init__(self, template_name, scene_name, options):
		super(TemplateCommmand, self).__init__()
		self.template_name = template_name
		self.scene_name = scene_name
		self.options = options

	def create_files(self):
		try:
			with open(FILE_HEADER) as f:
				content = f.readlines()
				info = [x.strip() for x in content]
				project = info[0]
				developer = info[1]
				company = info[2]
		except:
			project, developer, company = FileHeaderCommand().update_file_header()
		now = datetime.now()
		date = "{}/{}/{}".format(now.month, now.day, now.strftime("%y"))
		if self.template_name == Template.TemplateType.BASE:
			template = Template.BaseTemplate(self.scene_name, project, developer, company, date)
			template.create_files()
			print("Finish!")
		elif self.template_name == Template.TemplateType.LIST:
			model_text = pasteboard_read()
			try:
				model = Template().parse_model(model_text)
				template = Template.ListTemplate(model, self.options, self.scene_name, project, developer, company, date)
				template.create_files()
				print("Finish!")
			except:
				print('Invalid model text in clipboard.')
		elif self.template_name == Template.TemplateType.DETAIL:
			model_text = pasteboard_read()
			# try:
			model = Template().parse_model(model_text)
			if "--static" in self.options:
				template = Template.StaticDetailTemplate(model, self.options, self.scene_name, project, developer, company, date)
			else:
				template = Template.DetailTemplate(model, self.options, self.scene_name, project, developer, company, date)
			template.create_files()
			# 	print("Finish!")
			# except:
			# 	print('Invalid model text in clipboard.')
		else:
			print("Invalid template name.")


class JSONCommand(object):
	def __init__(self, model_name, json_text):
		super(JSONCommand, self).__init__()
		self.model_name = model_name
		self.json_text = json_text

	def create_models(self):
		# try:
		output = JSON(self.model_name, self.json_text).create_models()
		pasteboard_write(output)
		print("Text has been copied to clipboard.")
		# except:
		# 	print("Invalid json string in clipboard.")


class MockCommand(object):
	def __init__(self, protocol_text):
		super(MockCommand, self).__init__()
		self.protocol_text = protocol_text

	def create_mock(self):
		try:
			output = Mock(self.protocol_text).create_mock()
			pasteboard_write(output)
			print("Text has been copied to clipboard.")
		except:
			print("Invalid protocol text in clipboard.")


class APICommand(object):
	def __init__(self, api_name):
		super(APICommand, self).__init__()
		self.api_name = api_name

	def create_api(self):
		output = API(self.api_name).create_api()
		pasteboard_write(output)
		print("Text has been copied to clipboard.")


class UnitTestCommand(object):
	def __init__(self, vm_text):
		super(UnitTestCommand, self).__init__()
		self.vm_text = vm_text

	def create_tests(self):
		try:
			output = UnitTest(self.vm_text).create_tests()
			pasteboard_write(output)
			print("Text has been copied to clipboard.")
		except:
			print("Invalid view model text in clipboard.")


class BindViewModelCommand(object):
	def __init__(self, vm_text):
		super(BindViewModelCommand, self).__init__()
		self.vm_text = vm_text

	def create_bind_view_model(self):
		try:
			output = BindViewModel(self.vm_text).create_bind_view_model()
			pasteboard_write(output)
			print("Text has been copied to clipboard.")
		except:
			print("Invalid view model text in clipboard.")		


class InitCommand(object):

	def __init__(self, model_text):
		super(InitCommand, self).__init__()
		self.model_text = model_text
		
	def create_init(self):
		try:
			output = InitModel(self.model_text).create_init()
			pasteboard_write(output)
			print("Text has been copied to clipboard.")
		except:
			print("Invalid model text in clipboard.")	


#=================== Main ===================


def execute(args):
	command = args[0]
	if command == "t":
		command = "template"
	if command == Commands.HELP:
		HelpCommand().show_help()
	elif command == Commands.HEADER:
		FileHeaderCommand().update_file_header()
	elif command == Commands.TEMPLATE:
		if len(args) >= 3:
			template_name = args[1]
			scene_name = args[2]
			options = args[3:]
			TemplateCommmand(template_name, scene_name, options).create_files()
		else:
			print("Invalid params.")
	elif command == Commands.JSON:
		if len(args) >= 2:
			model_name = args[1]
			json = pasteboard_read()
			JSONCommand(model_name, json).create_models()
		else:
			print("Missing model name.")
	elif command == Commands.MOCK:
		protocol_text = pasteboard_read()
		MockCommand(protocol_text).create_mock()
	elif command == Commands.API:
		if len(args) >= 2:
			api_name = args[1]
			APICommand(api_name).create_api()
		else:
			print("Missing api name.")
	elif command == Commands.UNIT_TEST:
		vm_text = pasteboard_read()
		UnitTestCommand(vm_text).create_tests()
	elif command == Commands.BIND_VIEW_MODEL:
		vm_text = pasteboard_read()
		BindViewModelCommand(vm_text).create_bind_view_model()
	elif command == Commands.INIT:
		model_text = pasteboard_read()
		InitCommand(model_text).create_init()
	else:
		print("'{}' is not a valid command. See 'python it.py help'.".format(command))



