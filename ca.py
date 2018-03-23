# coding=utf-8
# Created by Tuan Truong on 2018-03-09.
# © 2018 Framgia.
# v1.1.1

import sys
import os
from datetime import datetime

class FileCreator(object):
	def __init__(self, name, project, developer, company, date):
		super(FileCreator, self).__init__()
		self.name = name
		self.project = project
		self.developer = developer
		self.company = company
		self.date = date

	def __file_header(self, class_name):
		file_name = class_name + ".swift"
		header = "//\n"
		header += "// {}\n".format(file_name)
		header += "// {}\n".format(self.project)
		header += "//\n"
		header += "// Created by {} on {}.\n".format(self.developer, self.date)
		now = datetime.now()
		header += "// Copyright © {} {}. All rights reserved.\n".format(now.year, self.company)
		header += "//\n"
		header += "\n"
		return header

	def create_files(self):
		print(" ")
		self.___make_dirs()
		self.__create_view_model()
		self.__create_navigator()
		self.__create_use_case_type()
		self.__create_use_case()
		self.__create_view_controller()
		self.__create_view_model_tests()
		self.__create_use_case_mock()
		self.__create_navigator_mock()
		self.__create_view_controller_tests()
		print(" ")

	def ___make_dirs(self):
		current_directory = os.getcwd()
		main_directory = os.path.join(current_directory, r'{}'.format(self.name))
		try: 
			os.makedirs(main_directory)
		except:
			pass
		else:
			test_directory = os.path.join(main_directory, "Test")
			try:
				os.makedirs(test_directory)
			except:
				pass

	def __create_view_model(self):
		class_name = self.name + "ViewModel"
		content = self.__file_header(class_name)
		content += "struct {0}: ViewModelType {{\n\n".format(class_name)
		content += "    struct Input {\n\n    }\n\n"
		content += "    struct Output {\n\n    }\n\n"
		content += "    let navigator: {}NavigatorType\n".format(self.name)
		content += "    let useCase: {}UseCaseType\n\n".format(self.name)
		content += "    func transform(_ input: Input) -> Output {\n        return Output()\n    }\n\n}\n"
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self.__create_file(file_path, file_name, content)

	def __create_navigator(self):
		class_name = self.name + "Navigator"
		protocol_name = class_name + "Type"
		content = self.__file_header(class_name)
		content += "protocol {0} {{\n\n}}\n\n".format(protocol_name)
		content += "struct {}: {} {{\n\n}}\n".format(class_name, protocol_name)
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self.__create_file(file_path, file_name, content)

	def __create_use_case_type(self):
		class_name = self.name + "UseCaseType"
		content = self.__file_header(class_name)
		content += "protocol {0} {{\n\n}}\n\n".format(class_name)
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self.__create_file(file_path, file_name, content)

	def __create_use_case(self):
		class_name = self.name + "UseCase"
		protocol_name = class_name + "Type"
		content = self.__file_header(class_name)
		content += "struct {}: {} {{\n\n}}\n".format(class_name, protocol_name)
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self.__create_file(file_path, file_name, content)

	def __create_view_controller(self):
		class_name = self.name + "ViewController"
		content = self.__file_header(class_name)
		content += "import UIKit\nimport Reusable\n\n"
		content += "final class {}: UIViewController, BindableType {{\n\n".format(class_name)
		content += "    var viewModel: {}ViewModel!\n\n".format(self.name)
		content += "    override func viewDidLoad() {\n        super.viewDidLoad()\n    }\n\n"
		content += "    func bindViewModel() {\n"
		content += "        let input = {}ViewModel.Input()\n".format(self.name)
		content += "        let output = viewModel.transform(input)\n"
		content += "    }\n\n}\n\n"
		content += "// MARK: - StoryboardSceneBased\n"
		content += "extension {}ViewController: StoryboardSceneBased {{\n".format(self.name)
		content += "    static var sceneStoryboard = UIStoryboard()\n}\n"
		file_name = class_name + ".swift"
		file_path = "{}/{}.swift".format(self.name, class_name)
		self.__create_file(file_path, file_name, content)

	def __create_view_model_tests(self):
		class_name = self.name + "ViewModelTests"
		content = self.__file_header(class_name)
		content += "@testable import {}\n".format(self.project)
		content += "import XCTest\nimport RxSwift\nimport RxBlocking\n\n"
		content += "final class {0}: XCTestCase {{\n\n".format(class_name)
		content += "    var viewModel: {}ViewModel!\n".format(self.name)
		content += "    var navigator: {}NavigatorMock!\n".format(self.name)
		content += "    var useCase: {}UseCaseMock!\n".format(self.name)
		content += "    var disposeBag: DisposeBag!\n\n"
		content += "    override func setUp() {\n"
		content += "        super.setUp()\n"
		content += "        navigator = {}NavigatorMock()\n".format(self.name)
		content += "        useCase = {}UseCaseMock()\n".format(self.name)
		content += "        viewModel = {}ViewModel(navigator: navigator, useCase: useCase)\n".format(self.name)
		content += "        disposeBag = DisposeBag()\n    }\n\n"
		content += "    func test_triggerInvoked_() {\n        // arrange\n"
		content += "        let input = {}ViewModel.Input()\n".format(self.name)
		content += "        let output = viewModel.transform(input)\n\n        // act\n\n"
		content += "        // assert\n        XCTAssert(true)\n    }\n\n}"
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self.__create_file(file_path, file_name, content)

	def __create_use_case_mock(self):
		class_name = self.name + "UseCaseMock"
		content = self.__file_header(class_name)
		content += "@testable import {}\n".format(self.project)
		content += "import RxSwift\n\n"
		content += "final class {0}: {1}UseCaseType {{\n\n}}\n".format(class_name, self.name)
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self.__create_file(file_path, file_name, content)

	def __create_navigator_mock(self):
		class_name = self.name + "NavigatorMock"
		content = self.__file_header(class_name)
		content += "@testable import {}\n\n".format(self.project)
		content += "final class {0}: {1}NavigatorType {{\n\n}}\n".format(class_name, self.name)
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self.__create_file(file_path, file_name, content)

	def __create_view_controller_tests(self):
		class_name = self.name + "ViewControllerTests"
		content = self.__file_header(class_name)
		content += "@testable import {}\n".format(self.project)
		content += "import XCTest\nimport Reusable\n\n"
		content += "final class {0}: XCTestCase {{\n\n".format(class_name)
		content += "    var viewController: {}ViewController!\n\n".format(self.name)
		content += "    override func setUp() {\n        super.setUp()\n"
		content += "        viewController = {}ViewController.instantiate()\n    }}\n\n".format(self.name)
		content += "    func test_ibOutlets() {\n"
		content += "        _ = viewController.view\n"
		content += "        XCTAssert(true)\n"
		content += "//        XCTAssertNotNil(viewController.tableView)\n"
		content += "    }\n\n}\n"
		file_name = class_name + ".swift"
		file_path = "{}/Test/{}.swift".format(self.name, class_name)
		self.__create_file(file_path, file_name, content)

	def __create_file(self, file_path, file_name, content):
		with open(file_path, "w") as f:
			f.write(content)
			print("    new file:   {}".format(file_path))

def create_files(name):
	now = datetime.now()
	date = "{}/{}/{}".format(now.month, now.day, now.strftime("%y"))
	file_name = "ca_info.txt"
	try:
		with open(file_name) as f:
			content = f.readlines()
			args = [x.strip() for x in content]
			project = args[0]
			developer = args[1]
			company = args[2]
	except:
		project = raw_input('Enter project name: ')
		developer = raw_input('Enter developer name: ')
		company = raw_input('Enter company name: ')
		content = "\n".join([project, developer, company])
		with open(file_name, "w") as f:	
			f.write(content)
	creator = FileCreator(name, project, developer, company, date)
	creator.create_files()

if len(sys.argv) > 1:
	name = sys.argv[1]
else:
	name = raw_input('Enter a scene name: ')
create_files(name)
print("Finish!")

