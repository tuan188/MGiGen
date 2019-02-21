# coding=utf-8

import re
import os
from jinja2 import Environment, PackageLoader
from datetime import datetime
from .str_helpers import upper_first_letter, lower_first_letter
from .constants import (SWIFT_TYPES_DEFAULT_VALUES,
                        SWIFT_TYPES_MOCK_VALUES,
                        SWIFT_TYPES)
from .file_helpers import create_file
from .config_cmd import ConfigCommand


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
            property_regex = re.compile(r'(?:let|var) (\w+): (.*)')
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

        @property
        def is_optional(self):
            return self.name.endswith("?")

        @property
        def is_array(self):
            return self.name.endswith("]") and ':' not in self.name

        @property
        def is_dictionary(self):
            return self.name.endswith("]") and ':' in self.name

        @property
        def is_observable(self):
            return self.name.startswith('Observable')

        @property
        def is_driver(self):
            return self.name.startswith('Driver')

        @property
        def default_value(self):
            if self.is_optional:
                value = "nil"
            elif self.is_array:
                value = "[]"
            elif self.is_dictionary:
                value = "[:]"
            elif self.name in SWIFT_TYPES:
                value = SWIFT_TYPES_DEFAULT_VALUES[self.name]
            elif self.is_observable:
                value = 'Observable.empty()'
            elif self.is_driver:
                value = 'Driver.empty()'
            else:
                value = "{}()".format(self.name)
            return value

        @property
        def mock_value(self):
            if self.is_optional:
                value = "nil"
            elif self.is_array:
                value = "[]"
            elif self.is_dictionary:
                value = "[:]"
            elif self.name in SWIFT_TYPES:
                value = SWIFT_TYPES_MOCK_VALUES[self.name]
            elif self.is_observable:
                value = 'Observable.empty()'
            elif self.is_driver:
                value = 'Driver.empty()'
            else:
                value = "{}()".format(self.name)
            return value

    class TemplateType:
        BASE = 'base'
        LIST = 'list'
        DETAIL = 'detail'
        SKELETON = 'skeleton'
        FORM = 'form'
        LOGIN = 'login'
        SETTING = 'setting'

    class Enum(object):
        def __init__(self, name, cases):
            super(Template.Enum, self).__init__()
            self.name = name
            self.name_variable = lower_first_letter(name)
            self.cases = cases
            self.cases_title = [upper_first_letter(c) for c in cases]
            self.case_count = len(cases)

    def parse_model(self, model_text):
        model_regex = re.compile(
            r'(?:struct|class|extension) (\w+)(?::\s)*(?:\w+,?\s?)* {([^}]+)'
        )
        match = model_regex.search(model_text)
        model_name = match.group(1)
        property_block = match.group(2)
        property_regex = re.compile(r'(?:let|var) (\w+): (.*)')
        properties = [Template.Property(m.group())
                      for m in property_regex.finditer(property_block)]
        return Template.Model(model_name, properties)

    def parse_enum(self, enum_text):
        enum_regex = re.compile(r'enum (\w+)[^{]* {([\d\D]*)}')
        match = enum_regex.search(enum_text)
        enum_name = match.group(1)
        enum_block = match.group(2)
        regex = re.compile(r'case (\w+)')
        cases = [m.group(1) for m in regex.finditer(enum_block)]
        return Template.Enum(enum_name, cases)

    # =============== BaseTemplate ===============

    class BaseTemplate(object):
        def __init__(self, options, name, project_info):
            super(Template.BaseTemplate, self).__init__()
            self.name = name
            self.project = project_info.project
            self.developer = project_info.developer
            self.company = project_info.company
            self.use_window = options['window']
            output_path = ConfigCommand().output_path()
            if output_path is None:
                output_path = '.'
            self.output_path = output_path
            self.env = Environment(
                loader=PackageLoader('igen_templates', 'base'),
                trim_blocks=True,
                lstrip_blocks=True
            )

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
            output_path = self._make_dirs()
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
            return output_path

        def _make_dirs(self):
            current_directory = os.getcwd() if self.output_path == '.' \
                                            else self.output_path
            main_directory = self._make_dir(current_directory, self.name)
            self._make_dir(main_directory, 'Test')
            return main_directory

        def _make_dir(self, current_directory, new_directory_name):
            directory = os.path.join(current_directory,
                                     r'{}'.format(new_directory_name))
            try:
                os.makedirs(directory)
            except Exception as e:
                print(e)
                pass
            return directory

        def _create_file_from_template(self,
                                       class_name,
                                       file_extension="swift",
                                       template_file=None,
                                       folder=None,
                                       has_file_header=True):
            if template_file is None:
                if file_extension:
                    template_file = '{}.{}'.format(class_name, file_extension)
                else:
                    template_file = class_name[len(self.name):]
            template = self.env.get_template(template_file)
            content = self._file_header(class_name) if has_file_header else ''
            content += self._content_from_template(template)
            if folder:
                folder = '{}/{}/{}'.format(self.output_path, self.name, folder)
            else:
                folder = '{}/{}'.format(self.output_path, self.name)
            file_path = create_file(
                content=content,
                file_name=class_name,
                file_extension=file_extension,
                folder=folder
            )
            if file_path is not None:
                print('    {}'.format(file_path))

        def _content_from_template(self, template):
            return template.render(
                name=self.name,
                project=self.project,
                use_window=self.use_window
            )

        def _create_view_model(self):
            scene_name = 'ViewModel'
            self._create_file_from_template(
                class_name=self.name + scene_name,
                template_file='{}.swift'.format(scene_name)
            )

        def _create_navigator(self):
            scene_name = 'Navigator'
            self._create_file_from_template(
                class_name=self.name + scene_name,
                template_file='{}.swift'.format(scene_name)
            )

        def _create_use_case(self):
            scene_name = 'UseCase'
            self._create_file_from_template(
                class_name=self.name + scene_name,
                template_file='{}.swift'.format(scene_name)
            )

        def _create_view_controller(self):
            scene_name = 'ViewController'
            self._create_file_from_template(
                class_name=self.name + scene_name,
                template_file='{}.swift'.format(scene_name)
            )

        def _create_assembler(self):
            scene_name = 'Assembler'
            self._create_file_from_template(
                class_name=self.name + scene_name,
                template_file='{}.swift'.format(scene_name)
            )

        # =============== UnitTests ===============

        def _create_view_model_tests(self):
            scene_name = 'ViewModelTests'
            self._create_file_from_template(
                class_name=self.name + scene_name,
                template_file='{}.swift'.format(scene_name),
                folder='Test'
            )

        def _create_use_case_mock(self):
            scene_name = 'UseCaseMock'
            self._create_file_from_template(
                class_name=self.name + scene_name,
                template_file='{}.swift'.format(scene_name),
                folder='Test'
            )

        def _create_navigator_mock(self):
            scene_name = 'NavigatorMock'
            self._create_file_from_template(
                class_name=self.name + scene_name,
                template_file='{}.swift'.format(scene_name),
                folder='Test'
            )

        def _create_view_controller_tests(self):
            scene_name = 'ViewControllerTests'
            self._create_file_from_template(
                class_name=self.name + scene_name,
                template_file='{}.swift'.format(scene_name),
                folder='Test'
            )

    # =============== ListTemplate ===============

    class ListTemplate(BaseTemplate):

        def __init__(self, model, options, name, project_info):
            super(Template.ListTemplate, self).__init__(
                options,
                name,
                project_info
            )
            self.model = model
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
            output_path = self._make_dirs()
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
            return output_path

        def _content_from_template(self, template):
            return template.render(
                name=self.name,
                project=self.project,
                use_window=self.use_window,
                model_name=self.model_name,
                model_variable=self.model_variable,
                properties=self.model.properties
            )

        def _create_view_model(self):
            self._create_file_from_template(
                class_name=self.name + 'ViewModel',
                template_file='SectionedViewModel.swift'
                              if self.is_sectioned_list
                              else 'ViewModel.swift'
            )

        def _create_item_view_model(self):
            self._create_file_from_template(
                class_name=self.model_name + 'ViewModel',
                template_file="ItemViewModel.swift"
            )

        def _create_view_controller(self):
            class_name = self.name + 'ViewController'
            if self.is_sectioned_list:
                if self.is_collection:
                    template_file = 'SectionedCollectionViewController.swift'
                else:
                    template_file = 'SectionedTableViewController.swift'
            else:
                if self.is_collection:
                    template_file = 'CollectionViewController.swift'
                else:
                    template_file = 'TableViewController.swift'
            self._create_file_from_template(
                class_name=class_name,
                template_file=template_file
            )

        def _create_table_view_cell(self):
            self._create_file_from_template(
                class_name=self.model_name + 'Cell',
                template_file='CollectionViewCell.swift'
                              if self.is_collection
                              else 'TableViewCell.swift'
            )

        # =============== UnitTests ===============

        def _create_view_model_tests(self):
            self._create_file_from_template(
                class_name=self.name + 'ViewModelTests',
                template_file='SectionedViewModelTests.swift'
                              if self.is_sectioned_list
                              else 'ViewModelTests.swift',
                folder='Test'
            )

        def _create_view_controller_tests(self):
            self._create_file_from_template(
                class_name=self.name + 'ViewControllerTests',
                template_file='CollectionViewControllerTests.swift'
                              if self.is_collection
                              else 'TableViewControllerTests.swift',
                folder='Test'
            )

        def _create_table_view_cell_tests(self):
            self._create_file_from_template(
                class_name='{}CellTests'.format(self.model_name),
                template_file='TableViewCellTests.swift',
                folder='Test'
            )

    # =============== DetailTemplate ===============

    class DetailTemplate(BaseTemplate):
        def __init__(self, model, options, name, project_info):
            super(Template.DetailTemplate, self).__init__(
                options,
                name,
                project_info
            )
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
            output_path = self._make_dirs()
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
            return output_path

        def _content_from_template(self, template):
            return template.render(
                name=self.name,
                project=self.project,
                use_window=self.use_window,
                model_name=self.model_name,
                model_variable=self.model_variable,
                properties=self.model.properties
            )

        def _create_cells(self):
            for p in self.model.properties:
                self._create_cell(p)

        def _create_cell(self, property):
            class_name = '{}{}Cell'.format(
                self.model_name,
                property.name_title
            )
            template = self.env.get_template('Cell.swift')
            content = self._file_header(class_name)
            content += template.render(
                model_name=self.model_name,
                property=property
            )
            file_path = create_file(
                content=content,
                file_name=class_name,
                file_extension='swift',
                folder='{}/{}'.format(self.output_path, self.name)
            )
            if file_path is not None:
                print('    {}'.format(file_path))

        # =============== UnitTests ===============

        def _create_cells_tests(self):
            self._create_file_from_template(
                class_name='{}CellsTests'.format(self.name),
                template_file='CellsTests.swift',
                folder='Test'
            )

    # =============== StaticDetailTemplate ===============

    class StaticDetailTemplate(DetailTemplate):

        def create_files(self):
            print('Successfully created files:')
            output_path = self._make_dirs()
            self._create_assembler()
            self._create_view_model()
            self._create_navigator()
            self._create_use_case()
            self._create_view_controller()
            self._create_view_model_tests()
            self._create_use_case_mock()
            self._create_navigator_mock()
            self._create_view_controller_tests()
            return output_path

        def _content_from_template(self, template):
            return template.render(
                name=self.name,
                project=self.project,
                use_window=self.use_window,
                model_name=self.model_name,
                model_variable=self.model_variable,
                properties=self.model.properties
            )

        def _create_view_model(self):
            self._create_file_from_template(
                class_name=self.name + 'ViewModel',
                template_file='StaticViewModel.swift'
            )

        def _create_view_controller(self):
            self._create_file_from_template(
                class_name=self.name + 'ViewController',
                template_file='StaticViewController.swift'
            )

        # =============== UnitTests ===============

        def _create_view_model_tests(self):
            self._create_file_from_template(
                class_name=self.name + 'ViewModelTests',
                template_file='StaticViewModelTests.swift',
                folder='Test'
            )

        def _create_view_controller_tests(self):
            self._create_file_from_template(
                class_name=self.name + 'ViewControllerTests',
                template_file='StaticViewControllerTests.swift',
                folder='Test'
            )

    # =============== SkeletonTemplate ===============

    class SkeletonTemplate(BaseTemplate):

        def __init__(self, options, name, project_info):
            super(Template.SkeletonTemplate, self).__init__(
                options,
                name,
                project_info
            )
            self.env = Environment(
                loader=PackageLoader('igen_templates', 'skeleton'),
                trim_blocks=True,
                lstrip_blocks=True
            )

        def _make_dirs(self):
            current_directory = os.getcwd() if self.output_path == '.' \
                                            else self.output_path
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
            return main_directory

        def create_files(self):
            print('Successfully created files:')
            output_path = self._make_dirs()
            self._create_podfile()
            self._create_localizable()
            self._create_swiftlint()
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
            return output_path

        def _content_from_template(self, template):
            return template.render(
                project=self.project
            )

        def _create_podfile(self):
            self._create_file_from_template(
                class_name='Podfile',
                file_extension=None,
                template_file='Podfile.txt',
                has_file_header=False
            )

        def _create_localizable(self):
            self._create_file_from_template(
                class_name='Localizable',
                file_extension='strings',
                template_file='Localizable.strings'
            )

        def _create_swiftlint(self):
            self._create_file_from_template(
                class_name='swiftlint',
                file_extension='yml',
                template_file='swiftlint.yml',
                has_file_header=False
            )

        def _create_UnitTestViewController(self):
            self._create_file_from_template(
                class_name='UnitTestViewController'
            )

        def _create_AppDelegate(self):
            self._create_file_from_template(
                class_name='AppDelegate'
            )

        def _create_BridgingHeader(self):
            self._create_file_from_template(
                class_name='{}-Bridging-Header'.format(self.project),
                file_extension='h',
                template_file='Bridging-Header.h'
            )

        def _create_assembler(self):
            self._create_file_from_template(
                class_name='Assembler',
                folder='Assembler'
            )

        def _create_utils(self):
            self._create_file_from_template(
                class_name='Utils',
                folder='Support'
            )

        def _create_UIViewController_(self):
            self._create_file_from_template(
                class_name='UIViewController+',
                folder='Extensions'
            )

        def _create_UIViewController_rx(self):
            self._create_file_from_template(
                class_name='UIViewController+Rx',
                folder='Extensions'
            )

        def _create_APIError(self):
            self._create_file_from_template(
                class_name='APIError',
                folder='Platform/Services/API'
            )

        def _create_APIService(self):
            self._create_file_from_template(
                class_name='APIService',
                folder='Platform/Services/API'
            )

        def _create_APIInput(self):
            self._create_file_from_template(
                class_name='APIInput',
                folder='Platform/Services/API'
            )

        def _create_APIOutput(self):
            self._create_file_from_template(
                class_name='APIOutput',
                folder='Platform/Services/API'
            )

        def _create_APIUrls(self):
            self._create_file_from_template(
                class_name='APIUrls',
                folder='Platform/Services/API'
            )

        def _create_AppAssembler(self):
            self._create_file_from_template(
                class_name='AppAssembler',
                folder='Scenes/App'
            )

        def _create_AppNavigator(self):
            self._create_file_from_template(
                class_name='AppNavigator',
                folder='Scenes/App'
            )

        def _create_AppUseCase(self):
            self._create_file_from_template(
                class_name='AppUseCase',
                folder='Scenes/App'
            )

        def _create_AppViewModel(self):
            self._create_file_from_template(
                class_name='AppViewModel',
                folder='Scenes/App'
            )

        def _create_Storyboards(self):
            self._create_file_from_template(
                class_name='Storyboards',
                folder='Scenes/Storyboards'
            )

    # =============== FormTemplate ===============

    class FormTemplate(BaseTemplate):
        def __init__(self, model, options, name, project_info):
            super(Template.FormTemplate, self).__init__(
                options,
                name,
                project_info
            )
            self.model = model
            self.model_name = self.model.name
            self.model_variable = lower_first_letter(self.model_name)
            self.submit = lower_first_letter(options['submit']) \
                if options['submit'] else 'submit'
            self.env = Environment(
                loader=PackageLoader('igen_templates', 'form'),
                trim_blocks=True,
                lstrip_blocks=True
            )

        def create_files(self):
            print('Successfully created files:')
            output_path = self._make_dirs()
            self._create_assembler()
            self._create_navigator()
            self._create_view_model()
            self._create_use_case()
            self._create_view_controller()
            # Test
            self._create_use_case_mock()
            self._create_navigator_mock()
            self._create_view_model_tests()
            self._create_view_controller_tests()
            return output_path

        def _content_from_template(self, template):
            return template.render(
                name=self.name,
                project=self.project,
                use_window=self.use_window,
                model_name=self.model_name,
                model_variable=self.model_variable,
                properties=self.model.properties,
                submit=self.submit
            )

    # =============== DynamicFormTemplate ===============

    class DynamicFormTemplate(BaseTemplate):
        def __init__(self, model, options, name, project_info):
            super(Template.DynamicFormTemplate, self).__init__(
                options,
                name,
                project_info
            )
            self.model = model
            self.model_name = self.model.name
            self.model_variable = lower_first_letter(self.model_name)
            self.submit = lower_first_letter(options['submit']) \
                if options['submit'] else 'submit'
            self.env = Environment(
                loader=PackageLoader('igen_templates', 'form'),
                trim_blocks=True,
                lstrip_blocks=True
            )

        def create_files(self):
            print('Successfully created files:')
            output_path = self._make_dirs()
            self._create_assembler()
            self._create_navigator()
            self._create_view_model()
            self._create_use_case()
            self._create_view_controller()
            self._create_cells()
            # Test
            self._create_use_case_mock()
            self._create_navigator_mock()
            self._create_view_model_tests()
            self._create_view_controller_tests()
            self._create_cells_tests()
            return output_path

        def _content_from_template(self, template):
            return template.render(
                name=self.name,
                project=self.project,
                use_window=self.use_window,
                model_name=self.model_name,
                model_variable=self.model_variable,
                properties=self.model.properties,
                submit=self.submit
            )

        def _create_view_model(self):
            self._create_file_from_template(
                class_name=self.name + 'ViewModel',
                template_file='DynamicViewModel.swift'
            )

        def _create_view_controller(self):
            self._create_file_from_template(
                class_name=self.name + 'ViewController',
                template_file='DynamicViewController.swift'
            )

        def _create_cells(self):
            for p in self.model.properties:
                self._create_cell(p)

        def _create_cell(self, property):
            class_name = '{}{}Cell'.format(self.name, property.name_title)
            template = self.env.get_template('Cell.swift')
            content = self._file_header(class_name)
            content += template.render(
                name=self.name,
                model_name=self.model_name,
                property=property
            )
            file_path = create_file(
                content=content,
                file_name=class_name,
                file_extension='swift',
                folder='{}/{}'.format(self.output_path, self.name)
            )
            if file_path is not None:
                print('    {}'.format(file_path))

        # =============== UnitTests ===============

        def _create_view_controller_tests(self):
            self._create_file_from_template(
                class_name='{}ViewControllerTests'.format(self.name),
                template_file='DynamicViewControllerTests.swift',
                folder='Test'
            )

        def _create_view_model_tests(self):
            self._create_file_from_template(
                class_name='{}ViewModelTests'.format(self.name),
                template_file='DynamicViewModelTests.swift',
                folder='Test'
            )

        def _create_cells_tests(self):
            self._create_file_from_template(
                class_name='{}CellsTests'.format(self.name),
                template_file='CellsTests.swift',
                folder='Test'
            )

    # =============== LoginTemplate ===============

    class LoginTemplate(BaseTemplate):
        def __init__(self, options, name, project_info):
            super(Template.LoginTemplate, self).__init__(
                options,
                name,
                project_info
            )
            self.env = Environment(
                loader=PackageLoader('igen_templates', 'login'),
                trim_blocks=True,
                lstrip_blocks=True
            )

        def create_files(self):
            print('Successfully created files:')
            output_path = self._make_dirs()
            self._create_assembler()
            self._create_navigator()
            self._create_view_model()
            self._create_use_case()
            self._create_view_controller()
            # Test
            self._create_use_case_mock()
            self._create_navigator_mock()
            self._create_view_model_tests()
            self._create_view_controller_tests()
            return output_path

    # =============== SettingTemplate ===============

    class SettingTemplate(BaseTemplate):
        def __init__(self, enum, options, name, project_info):
            super(Template.SettingTemplate, self).__init__(
                options,
                name,
                project_info
            )
            self.enum = enum
            self.is_sectioned_list = options['section']
            self.env = Environment(
                loader=PackageLoader('igen_templates', 'setting'),
                trim_blocks=True,
                lstrip_blocks=True
            )

        def create_files(self):
            print('Successfully created files:')
            output_path = self._make_dirs()
            self._create_assembler()
            self._create_navigator()
            self._create_view_model()
            self._create_use_case()
            self._create_view_controller()
            self._create_cell()
            # Test
            self._create_use_case_mock()
            self._create_navigator_mock()
            self._create_view_model_tests()
            self._create_view_controller_tests()
            self._create_cell_tests()
            return output_path

        def _content_from_template(self, template):
            return template.render(
                name=self.name,
                project=self.project,
                use_window=self.use_window,
                enum=self.enum
            )

        def _create_view_model(self):
            self._create_file_from_template(
                class_name=self.name + 'ViewModel',
                template_file='SectionedViewModel.swift'
                              if self.is_sectioned_list
                              else 'ViewModel.swift'
            )

        def _create_view_controller(self):
            self._create_file_from_template(
                class_name=self.name + 'ViewController',
                template_file='SectionedViewController.swift'
                              if self.is_sectioned_list
                              else 'ViewController.swift'
            )

        def _create_cell(self):
            self._create_file_from_template(
                class_name='{}Cell'.format(self.enum.name),
                template_file='Cell.swift'
            )

        # =============== UnitTests ===============

        def _create_view_model_tests(self):
            self._create_file_from_template(
                class_name='{}ViewModelTests'.format(self.name),
                template_file='SectionedViewModelTests.swift'
                              if self.is_sectioned_list
                              else 'ViewModelTests.swift',
                folder='Test'
            )

        def _create_cell_tests(self):
            self._create_file_from_template(
                class_name='{}CellTests'.format(self.enum.name),
                template_file='CellTests.swift',
                folder='Test'
            )
