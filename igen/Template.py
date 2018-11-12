# coding=utf-8

import re
import os
from jinja2 import Environment, PackageLoader
from datetime import datetime
from .str_helpers import upper_first_letter, lower_first_letter

class ProjectInfo(object):
	def __init__(self, project, developer, company):
		super(ProjectInfo, self).__init__()
		self.project = project
		self.developer = developer
		self.company = company
		

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
		BASE = 'base'
		LIST = 'list'
		DETAIL = 'detail'
		SKELETON = 'skeleton'

	def parse_model(self, model_text):
		model_regex = re.compile("(?:struct|class) (\w+) {((.|\n)*)}")
		match = model_regex.search(model_text)
		model_name = match.group(1)
		property_block = match.group(2)
		property_regex = re.compile("(?:let|var) (\w+): (.*)")
		properties = [Template.Property(p.group()) for p in property_regex.finditer(property_block)]
		return Template.Model(model_name, properties)


	#=================== BaseTemplate ===================

	class BaseTemplate(object):
		def __init__(self, name, project_info):
			super(Template.BaseTemplate, self).__init__()
			self.name = name
			self.project = project_info.project
			self.developer = project_info.developer
			self.company = project_info.company
			self.env = Environment(
				loader=PackageLoader('igen_templates', 'base'),
				trim_blocks=True,
				lstrip_blocks=True
			)

		def _create_file(self, class_name, content):
			file_path = "{}/{}.swift".format(self.name, class_name)
			self.__create_file(file_path, content)

		def _create_test_file(self, class_name, content):
			self._create_file_in_path("Test", class_name, content)

		def _create_file_in_path(self, file_path, class_name, content):
			file_path = "{}/{}/{}.swift".format(self.name, file_path, class_name)
			self.__create_file(file_path, content)	

		def __create_file(self, file_path, content):
			with open(file_path, "wb") as f:
				f.write(content.encode('utf8'))
				print("    {}".format(file_path))

		def _file_header(self, class_name):
			template = self.env.get_template("FileHeader.swift")
			now = datetime.now()
			date = "{}/{}/{}".format(now.month, now.day, now.strftime("%y"))
			header = template.render(
				class_name=class_name,
				project=self.project,
				developer=self.developer,
				created_date=date,
				copyright_year=now.year,
				company=self.company
			)
			return header + "\n\n"

		def create_files(self):
			print('Successfully created files:')
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

		def _make_dirs(self):
			current_directory = os.getcwd()
			main_directory = self._make_dir(current_directory, self.name)
			self._make_dir(main_directory, 'Test')

		def _make_dir(self, current_directory, new_directory_name):
			directory = os.path.join(current_directory, r'{}'.format(new_directory_name))
			try: 
				os.makedirs(directory)
			except:
				pass
			return directory

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

		def __init__(self, model, options, name, project_info):
			super(Template.ListTemplate, self).__init__(name, project_info)
			self.model = model
			self.options = options
			self.is_sectioned_list = options['section']
			self.is_collection = options['collection']
			self.model_name = self.model.name
			self.model_variable = lower_first_letter(self.model_name)
			self.env = Environment(
				loader=PackageLoader('igen_templates', 'list'),
				trim_blocks=True,
				lstrip_blocks=True
			)

		def create_files(self):
			print('Successfully created files:')
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
		def __init__(self, model, options, name, project_info):
			super(Template.DetailTemplate, self).__init__(name, project_info)
			self.model = model
			self.model_name = self.model.name
			self.model_variable = lower_first_letter(self.model_name)
			self.env = Environment(
				loader=PackageLoader('igen_templates', 'detail'),
				trim_blocks=True,
				lstrip_blocks=True
			)

		def create_files(self):
			print('Successfully created files:')
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

		def _create_assembler(self):
			class_name = self.name + "Assembler"
			template = self.env.get_template("Assembler.swift")
			content = self._file_header(class_name)
			content += template.render(
				name=self.name,
				model_name=self.model_name,
				model_variable=self.model_variable
			)
			self._create_file(class_name, content)

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
			print('Successfully created files:')
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


	#=================== SkeletonTemplate ===================

	class SkeletonTemplate(BaseTemplate):

		def __init__(self, name, project_info):
			super(Template.SkeletonTemplate, self).__init__(name, project_info)
			self.env = Environment(
				loader=PackageLoader('igen_templates', 'skeleton'),
				trim_blocks=True,
				lstrip_blocks=True
			)

		def _make_dirs(self):
			current_directory = os.getcwd()
			main_directory = self._make_dir(current_directory, self.name)
			self._make_dir(main_directory, "Assembler")
			self._make_dir(main_directory, "Extensions")
			self._make_dir(main_directory, "Support")
			domain_directory = self._make_dir(main_directory, "Domain")
			self._make_dir(domain_directory, "Model")
			platform_directory = self._make_dir(main_directory, "Platform")
			self._make_dir(platform_directory, "Repositories")
			services_directory = self._make_dir(platform_directory, "Services")
			self._make_dir(services_directory, "API")
			scenes_directory = self._make_dir(main_directory, "Scenes")
			self._make_dir(scenes_directory, "App")
			self._make_dir(scenes_directory, "Storyboards")

		def create_files(self):
			print('Successfully created files:')
			self._make_dirs()
			self._create_podfile()
			self._create_UnitTestViewController()
			self._create_AppDelegate()
			self._create_BridgingHeader()
			self._create_assembler()
			self._create_utils()
			self._create_UIViewController_()
			self._create_UIViewController_rx()
			self._create_APIError()
			self._create_APIService()
			self._create_APIInput()
			self._create_APIOutput()
			self._create_APIUrls()
			self._create_AppAssembler()
			self._create_AppNavigator()
			self._create_AppUseCase()
			self._create_AppViewModel()
			self._create_Storyboards()

		def _create_podfile(self):
			class_name = "Podfile"
			template = self.env.get_template("Podfile.swift")
			content = template.render(
				project=self.project
			)
			file_path = "{}/{}".format(self.name, class_name)
			Template.BaseTemplate._BaseTemplate__create_file(self, file_path, content)

		def _create_UnitTestViewController(self):
			class_name = "UnitTestViewController"
			template = self.env.get_template("UnitTestViewController.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file(class_name, content)

		def _create_AppDelegate(self):
			class_name = "AppDelegate"
			template = self.env.get_template("AppDelegate.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file(class_name, content)

		def _create_BridgingHeader(self):
			class_name = "{}-Bridging-Header".format(self.project)
			template = self.env.get_template("Bridging-Header.swift")
			content = self._file_header(class_name)
			content += template.render()
			file_path = "{}/{}.h".format(self.name, class_name)
			Template.BaseTemplate._BaseTemplate__create_file(self, file_path, content)

		def _create_assembler(self):
			class_name = "Assembler"
			template = self.env.get_template("Assembler.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Assembler", class_name, content)

		def _create_utils(self):
			class_name = "Utils"
			template = self.env.get_template("Utils.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Support", class_name, content)

		def _create_UIViewController_(self):
			class_name = "UIViewController+"
			template = self.env.get_template("UIViewController+.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Extensions", class_name, content)

		def _create_UIViewController_rx(self):
			class_name = "UIViewController+Rx"
			template = self.env.get_template("UIViewController+Rx.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Extensions", class_name, content)

		def _create_APIError(self):
			class_name = "APIError"
			template = self.env.get_template("APIError.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Platform/Services/API", class_name, content)

		def _create_APIService(self):
			class_name = "APIService"
			template = self.env.get_template("APIService.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Platform/Services/API", class_name, content)

		def _create_APIInput(self):
			class_name = "APIInput"
			template = self.env.get_template("APIInput.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Platform/Services/API", class_name, content)

		def _create_APIOutput(self):
			class_name = "APIOutput"
			template = self.env.get_template("APIOutput.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Platform/Services/API", class_name, content)

		def _create_APIUrls(self):
			class_name = "APIUrls"
			template = self.env.get_template("APIUrls.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Platform/Services/API", class_name, content)

		def _create_AppAssembler(self):
			class_name = "AppAssembler"
			template = self.env.get_template("AppAssembler.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Scenes/App", class_name, content)

		def _create_AppNavigator(self):
			class_name = "AppNavigator"
			template = self.env.get_template("AppNavigator.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Scenes/App", class_name, content)

		def _create_AppUseCase(self):
			class_name = "AppUseCase"
			template = self.env.get_template("AppUseCase.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Scenes/App", class_name, content)

		def _create_AppViewModel(self):
			class_name = "AppViewModel"
			template = self.env.get_template("AppViewModel.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Scenes/App", class_name, content)

		def _create_Storyboards(self):
			class_name = "Storyboards"
			template = self.env.get_template("Storyboards.swift")
			content = self._file_header(class_name)
			content += template.render()
			self._create_file_in_path("Scenes/Storyboards", class_name, content)

		






