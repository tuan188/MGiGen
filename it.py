# coding=utf-8
# Created by Tuan Truong on 2018-05-24.
# © 2018 Framgia.
# v1.0.0

import sys
import os
from datetime import datetime
import subprocess
import re
from collections import OrderedDict
import json

#=================== Helpers ===================

def pasteboard_read():
	return subprocess.check_output('pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

def pasteboard_write(output):
	process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
	process.communicate(output.encode('utf-8'))

def camel_case(st):
	output = ''.join(x for x in st.title() if x.isalpha())
	return output[0].lower() + output[1:]

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
			self.name_title = self.name.title()
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

	def _parse_model(self, model_text):
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

		def _file_header(self, class_name):
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
			self._make_dirs()
			self._create_view_model()
			self._create_navigator()
			self._create_use_case()
			self._create_view_controller()
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
			else:
				test_directory = os.path.join(main_directory, "Test")
				try:
					os.makedirs(test_directory)
				except:
					pass

		def _create_view_model(self):
			class_name = self.name + "ViewModel"
			content = self._file_header(class_name)
			content += "struct {0}: ViewModelType {{\n\n".format(class_name)
			content += "    struct Input {\n\n    }\n\n"
			content += "    struct Output {\n\n    }\n\n"
			content += "    let navigator: {}NavigatorType\n".format(self.name)
			content += "    let useCase: {}UseCaseType\n\n".format(self.name)
			content += "    func transform(_ input: Input) -> Output {\n"
			content += "        return Output()\n"
			content += "    }\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_navigator(self):
			class_name = self.name + "Navigator"
			protocol_name = class_name + "Type"
			content = self._file_header(class_name)
			content += "protocol {0} {{\n\n}}\n\n".format(protocol_name)
			content += "struct {}: {} {{\n\n}}\n".format(class_name, protocol_name)
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_use_case(self):
			class_name = self.name + "UseCase"
			protocol_name = class_name + "Type"
			content = self._file_header(class_name)
			content += "protocol {0} {{\n\n}}\n\n".format(protocol_name)
			content += "struct {}: {} {{\n\n}}\n".format(class_name, protocol_name)
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_view_controller(self):
			class_name = self.name + "ViewController"
			content = self._file_header(class_name)
			content += "import UIKit\nimport Reusable\n\n"
			content += "final class {}: UIViewController, BindableType {{\n\n".format(class_name)
			content += "    var viewModel: {}ViewModel!\n\n".format(self.name)
			content += "    override func viewDidLoad() {\n"
			content += "        super.viewDidLoad()\n"
			content += "    }\n\n"
			content += "    deinit {\n"
			content += "        logDeinit()\n"
			content += "    }\n\n"
			content += "    func bindViewModel() {\n"
			content += "        let input = {}ViewModel.Input()\n".format(self.name)
			content += "        let output = viewModel.transform(input)\n"
			content += "    }\n\n}\n\n"
			content += "// MARK: - StoryboardSceneBased\n"
			content += "extension {}ViewController: StoryboardSceneBased {{\n".format(self.name)
			content += "    // TODO: - Update storyboard\n"
			content += "    static var sceneStoryboard = UIStoryboard()\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_view_model_tests(self):
			class_name = self.name + "ViewModelTests"
			content = self._file_header(class_name)
			content += "@testable import {}\n".format(self.project)
			content += "import XCTest\nimport RxSwift\nimport RxBlocking\n\n"
			content += "final class {0}: XCTestCase {{\n\n".format(class_name)
			content += "    private var viewModel: {}ViewModel!\n".format(self.name)
			content += "    private var navigator: {}NavigatorMock!\n".format(self.name)
			content += "    private var useCase: {}UseCaseMock!\n".format(self.name)
			content += "    private var disposeBag: DisposeBag!\n\n"
			content += "    override func setUp() {\n"
			content += "        super.setUp()\n"
			content += "        navigator = {}NavigatorMock()\n".format(self.name)
			content += "        useCase = {}UseCaseMock()\n".format(self.name)
			content += "        viewModel = {}ViewModel(navigator: navigator, useCase: useCase)\n".format(self.name)
			content += "        disposeBag = DisposeBag()\n"
			content += "    }\n\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_use_case_mock(self):
			class_name = self.name + "UseCaseMock"
			content = self._file_header(class_name)
			content += "@testable import {}\n".format(self.project)
			content += "import RxSwift\n\n"
			content += "final class {0}: {1}UseCaseType {{\n\n}}\n".format(class_name, self.name)
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_navigator_mock(self):
			class_name = self.name + "NavigatorMock"
			content = self._file_header(class_name)
			content += "@testable import {}\n\n".format(self.project)
			content += "final class {0}: {1}NavigatorType {{\n\n}}\n".format(class_name, self.name)
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_view_controller_tests(self):
			class_name = self.name + "ViewControllerTests"
			content = self._file_header(class_name)
			content += "@testable import {}\n".format(self.project)
			content += "import XCTest\nimport Reusable\n\n"
			content += "final class {0}: XCTestCase {{\n\n".format(class_name)
			content += "    var viewController: {}ViewController!\n\n".format(self.name)
			content += "    override func setUp() {\n"
			content += "        super.setUp()\n"
			content += "        viewController = {}ViewController.instantiate()\n".format(self.name)
			content += "    }\n\n"
			content += "    func test_ibOutlets() {\n"
			content += "        _ = viewController.view\n"
			content += "        XCTAssert(true)\n"
			content += "//        XCTAssertNotNil(viewController.tableView)\n"
			content += "    }\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_file(self, file_path, file_name, content):
			with open(file_path, "w") as f:
				f.write(content)
				print("        new file:   {}".format(file_path))

	#=================== ListTemplate ===================

	class ListTemplate(BaseTemplate):

		def __init__(self, model, options, name, project, developer, company, date):
			super(Template.ListTemplate, self).__init__(name, project, developer, company, date)
			self.model = model
			self.options = options
			self.is_sectioned_list = "--section" in options
			self.model_name = self.model.name
			self.model_variable = camel_case(self.model_name)

		def create_files(self):
			print(" ")
			self._make_dirs()
			self._create_view_model()
			self._create_navigator()
			self._create_use_case()
			self._create_view_controller()
			self._create_table_view_cell()
			self._create_view_model_tests()
			self._create_use_case_mock()
			self._create_navigator_mock()
			self._create_view_controller_tests()
			self._create_table_view_cell_tests()
			print(" ")

		def _create_view_model(self):
			class_name = self.name + "ViewModel"
			content = self._file_header(class_name)
			content += "struct {0}: ViewModelType {{\n".format(class_name)
			content += "    struct Input {\n"
			content += "        let loadTrigger: Driver<Void>\n"
			content += "        let reloadTrigger: Driver<Void>\n"
			content += "        let loadMoreTrigger: Driver<Void>\n"
			content += "        let select{}Trigger: Driver<IndexPath>\n".format(self.model_name)
			content += "    }\n\n"
			content += "    struct Output {\n"
			content += "        let error: Driver<Error>\n"
			content += "        let loading: Driver<Bool>\n"
			content += "        let refreshing: Driver<Bool>\n"
			content += "        let loadingMore: Driver<Bool>\n"
			content += "        let fetchItems: Driver<Void>\n"
			if self.is_sectioned_list:
				content += "        let {}Sections: Driver<[{}Section]>\n".format(self.model_variable, self.model_name)
			else:
				content += "        let {}List: Driver<[{}Model]>\n".format(self.model_variable, self.model_name)
			content += "        let selected{}: Driver<Void>\n".format(self.model_name)
			content += "        let isEmptyData: Driver<Bool>\n"
			content += "    }\n\n"
			content += "    struct {}Model {{\n".format(self.model_name)
			content += "        let {}: {}\n".format(self.model_variable, self.model_name)
			content += "    }\n\n"
			if self.is_sectioned_list:
				content += "    struct {}Section {{\n".format(self.model_name)
				content += "        let header: String\n"
				content += "        let {}List: [{}Model]\n".format(self.model_variable, self.model_name)
				content += "    }\n\n"
			content += "    let navigator: {}NavigatorType\n".format(self.name)
			content += "    let useCase: {}UseCaseType\n\n".format(self.name)
			content += "    func transform(_ input: Input) -> Output {\n"
			content += "        let loadMoreOutput = setupLoadMorePaging(\n"
			content += "            loadTrigger: input.loadTrigger,\n"
			content += "            getItems: useCase.get{}List,\n".format(self.model_name)
			content += "            refreshTrigger: input.reloadTrigger,\n"
			content += "            refreshItems: useCase.get{}List,\n".format(self.model_name)
			content += "            loadMoreTrigger: input.loadMoreTrigger,\n"
			content += "            loadMoreItems: useCase.loadMore{}List)\n".format(self.model_name)
			content += "        let (page, fetchItems, loadError, loading, refreshing, loadingMore) = loadMoreOutput\n\n"
			if self.is_sectioned_list:
				content += "        let {}Sections = page\n".format(self.model_variable)
				content += "            .map {{ $0.items.map {{ {}Model({}: $0) }} }}\n".format(self.model_name, self.model_variable)
				content += '            .map {{ [{}Section(header: "Section1", {}List: $0)] }}\n'.format(self.model_name, self.model_variable)
				content += "            .asDriverOnErrorJustComplete()\n"
			else:
				content += "        let {}List = page\n".format(self.model_variable)
				content += "            .map {{ $0.items.map {{ {}Model({}: $0) }} }}\n".format(self.model_name, self.model_variable)
				content += "            .asDriverOnErrorJustComplete()\n\n"
			content += "        let selected{} = input.select{}Trigger\n".format(self.model_name, self.model_name)
			if self.is_sectioned_list:
				content += "            .withLatestFrom({}Sections) {{\n".format(self.model_variable)
				content += "                return ($0, $1)\n"
				content += "            }\n"
				content += "            .map {{ params -> {}Model in\n".format(self.model_name)
				content += "                let (indexPath, {}Sections) = params\n".format(self.model_variable)
				content += "                return {}Sections[indexPath.section].{}List[indexPath.row]\n".format(self.model_variable, self.model_variable)
				content += "            }\n"
			else:
				content += "            .withLatestFrom({}List) {{\n".format(self.model_variable)
				content += "                return ($0, $1)\n"
				content += "            }\n"
				content += "            .map {{ indexPath, {}List in\n".format(self.model_variable)
				content += "                return {}List[indexPath.row]\n".format(self.model_variable)
				content += "            }\n"
			content += "            .do(onNext: {{ {} in\n".format(self.model_variable)
			content += "                self.navigator.to{}Detail({}: {}.{})\n".format(self.model_name, self.model_variable, self.model_variable, self.model_variable)
			content += "            })\n"
			content += "            .mapToVoid()\n\n"
			if self.is_sectioned_list:
				content += "        let isEmptyData = Driver.combineLatest({}Sections, loading)\n".format(self.model_variable)
			else:
				content += "        let isEmptyData = Driver.combineLatest({}List, loading)\n".format(self.model_variable)
			content += "            .filter { !$0.1 }\n"
			content += "            .map { $0.0.isEmpty }\n\n"
			content += "        return Output(\n"
			content += "            error: loadError,\n"
			content += "            loading: loading,\n"
			content += "            refreshing: refreshing,\n"
			content += "            loadingMore: loadingMore,\n"
			content += "            fetchItems: fetchItems,\n"
			if self.is_sectioned_list:
				content += "            {}Sections: {}Sections,\n".format(self.model_variable, self.model_variable)
			else:
				content += "            {}List: {}List,\n".format(self.model_variable, self.model_variable)
			content += "            selected{}: selected{},\n".format(self.model_name, self.model_name)
			content += "            isEmptyData: isEmptyData\n"
			content += "        )\n"
			content += "    }\n"
			content += "}\n\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_use_case(self):
			class_name = self.name + "UseCase"
			protocol_name = class_name + "Type"
			content = self._file_header(class_name)
			content += "protocol {0} {{\n".format(protocol_name)
			content += "    func get{}List() -> Observable<PagingInfo<{}>>\n".format(self.model_name, self.model_name)
			content += "    func loadMore{}List(page: Int) -> Observable<PagingInfo<{}>>\n".format(self.model_name, self.model_name)
			content += "}\n\n"
			content += "struct {}: {} {{\n".format(class_name, protocol_name)
			content += "    func get{}List() -> Observable<PagingInfo<{}>> {{\n".format(self.model_name, self.model_name)
			content += "        return loadMore{}List(page: 1)\n".format(self.model_name)
			content += "    }\n\n"
			content += "    func loadMore{}List(page: Int) -> Observable<PagingInfo<{}>> {{\n".format(self.model_name, self.model_name)
			content += "        return Observable.empty()\n"
			content += "    }\n"
			content += "}\n\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_navigator(self):
			class_name = self.name + "Navigator"
			protocol_name = class_name + "Type"
			content = self._file_header(class_name)
			content += "protocol {0} {{\n".format(protocol_name)
			content += "    func to{}()\n".format(self.name)
			content += "    func to{}Detail({}: {})\n".format(self.model_name, self.model_variable, self.model_name)
			content += "}\n\n"
			content += "struct {}: {} {{\n".format(class_name, protocol_name)
			content += "    unowned let navigationController: UINavigationController\n\n"
			content += "    func to{}() {{\n".format(self.name)
			content += "        let vc = {}ViewController.instantiate()\n".format(self.name)
			content += "        let vm = {}ViewModel(navigator: self, useCase: {}UseCase())\n".format(self.name, self.name)
			content += "        vc.bindViewModel(to: vm)\n"
			content += "        navigationController.pushViewController(vc, animated: true)\n"
			content += "    }\n\n"
			content += "    func to{}Detail({}: {}) {{\n\n".format(self.model_name, self.model_variable, self.model_name)
			content += "    }\n"
			content += "}\n\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_view_controller(self):
			class_name = self.name + "ViewController"
			content = self._file_header(class_name)
			content += "import UIKit\nimport Reusable\n\n"
			if self.is_sectioned_list:
				content += "import RxDataSources\n"
			content += "final class {}: UIViewController, BindableType {{\n".format(class_name)
			content += "    @IBOutlet weak var tableView: LoadMoreTableView!\n"
			content += "    var viewModel: {}ViewModel!\n\n".format(self.name)
			if self.is_sectioned_list:
				content += "    fileprivate typealias {}SectionModel = SectionModel<String, {}ViewModel.{}Model>\n".format(self.model_name, self.name, self.model_name)
				content += "    fileprivate var dataSource: RxTableViewSectionedReloadDataSource<{}SectionModel>!\n".format(self.model_name)
			content += "    override func viewDidLoad() {\n"
			content += "        super.viewDidLoad()\n"
			content += "        configView()\n"
			content += "    }\n\n"
			content += "    private func configView() {\n"
			content += "        tableView.do {\n"
			content += "            $0.loadMoreDelegate = self\n"
			content += "            $0.estimatedRowHeight = 550\n"
			content += "            $0.rowHeight = UITableViewAutomaticDimension\n"
			content += "            $0.register(cellType: {}Cell.self)\n".format(self.model_name)
			content += "        }\n"
			content += "    }\n\n"
			content += "    deinit {\n"
			content += "        logDeinit()\n"
			content += "    }\n\n"
			content += "    func bindViewModel() {\n"
			content += "        let input = {}ViewModel.Input(\n".format(self.name)
			content += "            loadTrigger: Driver.just(()),\n"
			content += "            reloadTrigger: tableView.refreshTrigger,\n"
			content += "            loadMoreTrigger: tableView.loadMoreTrigger,\n"
			content += "            select{}Trigger: tableView.rx.itemSelected.asDriver()\n".format(self.model_name)
			content += "        )\n"
			content += "        let output = viewModel.transform(input)\n"
			if self.is_sectioned_list:
				content += "        dataSource = RxTableViewSectionedReloadDataSource<{}SectionModel>(\n".format(self.model_name)
				content += "            configureCell: {{ (_, tableView, indexPath, {}) -> UITableViewCell in\n".format(self.model_variable)
				content += "                return tableView.dequeueReusableCell(for: indexPath, cellType: {}Cell.self).then {{\n".format(self.model_name)
				content += "                    $0.configView(with: {})\n".format(self.model_variable)
				content += "                }\n"
				content += "            },\n"
				content += "            titleForHeaderInSection: { dataSource, section in\n"
				content += "                return dataSource.sectionModels[section].model\n"
				content += "            })\n"
				content += "        output.{}Sections\n".format(self.model_variable)
				content += "            .map {\n"
				content += "                $0.map { section in\n"
				content += "                    {}SectionModel(model: section.header, items: section.{}List)\n".format(self.model_name, self.model_variable)
				content += "                }\n"
				content += "            }\n"
				content += "            .drive(tableView.rx.items(dataSource: dataSource))\n"
				content += "            .disposed(by: rx.disposeBag)\n"
			else:
				content += "        output.{}List\n".format(self.model_variable)
				content += "            .drive(tableView.rx.items) {{ tableView, index, {} in\n".format(self.model_variable)
				content += "                return tableView.dequeueReusableCell(\n"
				content += "                    for: IndexPath(row: index, section: 0),\n"
				content += "                    cellType: {}Cell.self)\n".format(self.model_name)
				content += "                    .then {\n"
				content += "                        $0.configView(with: {})\n".format(self.model_variable)
				content += "                    }\n"
				content += "            }\n"
				content += "            .disposed(by: rx.disposeBag)\n"
			content += "        output.error\n"
			content += "            .drive(rx.error)\n"
			content += "            .disposed(by: rx.disposeBag)\n"
			content += "        output.loading\n"
			content += "            .drive(rx.isLoading)\n"
			content += "            .disposed(by: rx.disposeBag)\n"
			content += "        output.refreshing\n"
			content += "            .drive(tableView.refreshing)\n"
			content += "            .disposed(by: rx.disposeBag)\n"
			content += "        output.loadingMore\n"
			content += "            .drive(tableView.loadingMore)\n"
			content += "            .disposed(by: rx.disposeBag)\n"
			content += "        output.fetchItems\n"
			content += "            .drive()\n"
			content += "            .disposed(by: rx.disposeBag)\n"
			content += "        output.selected{}\n".format(self.model_name)
			content += "            .drive()\n"
			content += "            .disposed(by: rx.disposeBag)\n"
			content += "        output.isEmptyData\n"
			content += "            .drive()\n"
			content += "            .disposed(by: rx.disposeBag)\n"
			content += "    }\n\n}\n\n"
			content += "// MARK: - UITableViewDelegate\n"
			content += "extension {}ViewController: UITableViewDelegate {{\n".format(self.name)
			content += "    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {\n"
			content += "        tableView.deselectRow(at: indexPath, animated: true)\n"
			content += "    }\n"
			content += "}\n\n"
			content += "// MARK: - StoryboardSceneBased\n"
			content += "extension {}ViewController: StoryboardSceneBased {{\n".format(self.name)
			content += "    // TODO: - Update storyboard\n"
			content += "    static var sceneStoryboard = UIStoryboard()\n}\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_table_view_cell(self):
			model = self.model
			class_name = self.model_name + "Cell"
			content = self._file_header(class_name)
			content += "import UIKit\n\n"
			content += "final class {}Cell: UITableViewCell, NibReusable {{\n".format(self.model_name)
			for p in model.properties:
				if p.name != "id":
					if p.is_url:
						content += "    @IBOutlet weak var {}ImageView: UIImageView!\n".format(p.name)
					else:
						content += "    @IBOutlet weak var {}Label: UILabel!\n".format(p.name)
			content += "\n"
			content += "    override func awakeFromNib() {\n"
			content += "        super.awakeFromNib()\n"
			content += "    }\n\n"
			content += "    override func prepareForReuse() {\n"
			content += "        super.prepareForReuse()\n"
			content += "        configView(with: nil)\n"
			content += "    }\n\n"
			content += "    func configView(with model: {}ViewModel.{}Model?) {{\n".format(self.name, self.model_name)
			content += "        if let model = model {\n\n"
			content += "        } else {\n"
			for p in model.properties:
				if p.name != "id":
					if p.is_url:
						content += "            {}ImageView.image = nil\n".format(p.name)
					else:
						content += '            {}Label.text = ""\n'.format(p.name)
			content += "        }\n"
			content += "    }\n"
			content += "}\n\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_view_model_tests(self):
			class_name = self.name + "ViewModelTests"
			list_name = ("{}Sections" if self.is_sectioned_list else "{}List").format(self.model_variable)
			content = self._file_header(class_name)
			content += "@testable import {}\n".format(self.project)
			content += "import XCTest\nimport RxSwift\nimport RxBlocking\n\n"
			content += "final class {}: XCTestCase {{\n".format(class_name)
			content += "    private var viewModel: {}ViewModel!\n".format(self.name)
			content += "    private var navigator: {}NavigatorMock!\n".format(self.name)
			content += "    private var useCase: {}UseCaseMock!\n".format(self.name)
			content += "    private var disposeBag: DisposeBag!\n"
			content += "    private var input: {}ViewModel.Input!\n".format(self.name)
			content += "    private var output: {}ViewModel.Output!\n".format(self.name)
			content += "    private let loadTrigger = PublishSubject<Void>()\n"
			content += "    private let reloadTrigger = PublishSubject<Void>()\n"
			content += "    private let loadMoreTrigger = PublishSubject<Void>()\n"
			content += "    private let select{}Trigger = PublishSubject<IndexPath>()\n\n".format(self.model_name)
			content += "    override func setUp() {\n"
			content += "        super.setUp()\n"
			content += "        navigator = {}NavigatorMock()\n".format(self.name)
			content += "        useCase = {}UseCaseMock()\n".format(self.name)
			content += "        viewModel = {}ViewModel(navigator: navigator, useCase: useCase)\n".format(self.name)
			content += "        disposeBag = DisposeBag()\n"
			content += "        input = {}ViewModel.Input(\n".format(self.name)
			content += "            loadTrigger: loadTrigger.asDriverOnErrorJustComplete(),\n"
			content += "            reloadTrigger: reloadTrigger.asDriverOnErrorJustComplete(),\n"
			content += "            loadMoreTrigger: loadMoreTrigger.asDriverOnErrorJustComplete(),\n"
			content += "            select{}Trigger: select{}Trigger.asDriverOnErrorJustComplete()\n".format(self.model_name, self.model_name)
			content += "        )\n"
			content += "        output = viewModel.transform(input)\n"
			content += "        output.error.drive().disposed(by: disposeBag)\n"
			content += "        output.loading.drive().disposed(by: disposeBag)\n"
			content += "        output.refreshing.drive().disposed(by: disposeBag)\n"
			content += "        output.loadingMore.drive().disposed(by: disposeBag)\n"
			content += "        output.fetchItems.drive().disposed(by: disposeBag)\n"
			content += "        output.{}.drive().disposed(by: disposeBag)\n".format(list_name)
			content += "        output.selected{}.drive().disposed(by: disposeBag)\n".format(self.model_name)
			content += "        output.isEmptyData.drive().disposed(by: disposeBag)\n"
			content += "    }\n\n"
			content += "    func test_loadTriggerInvoked_get{}List() {{\n".format(self.model_name)
			content += "        // act\n"
			content += "        loadTrigger.onNext(())\n"
			content += "        let {} = try? output.{}.toBlocking(timeout: 1).first()\n".format(list_name, list_name)
			content += "        \n"
			content += "        // assert\n"
			content += "        XCTAssert(useCase.get{}List_Called)\n".format(self.model_name)
			if self.is_sectioned_list:
				content += "        XCTAssertEqual({}??[0].{}List.count, 1)\n".format(list_name, self.model_variable)
			else:
				content += "        XCTAssertEqual({}??.count, 1)\n".format(list_name)
			content += "    }\n\n"
			content += "    func test_loadTriggerInvoked_get{}List_failedShowError() {{\n".format(self.model_name)
			content += "        // arrange\n"
			content += "        let get{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
			content += "        useCase.get{}List_ReturnValue = get{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
			content += "        // act\n"
			content += "        loadTrigger.onNext(())\n"
			content += "        get{}List_ReturnValue.onError(TestError())\n".format(self.model_name)
			content += "        let error = try? output.error.toBlocking(timeout: 1).first()\n\n"
			content += "        // assert\n"
			content += "        XCTAssert(useCase.get{}List_Called)\n".format(self.model_name)
			content += "        XCTAssert(error is TestError)\n"
			content += "    }\n\n"
			content += "    func test_reloadTriggerInvoked_get{}List() {{\n".format(self.model_name)
			content += "        // act\n"
			content += "        reloadTrigger.onNext(())\n"
			content += "        let {} = try? output.{}.toBlocking(timeout: 1).first()\n\n".format(list_name, list_name)
			content += "        // assert\n"
			content += "        XCTAssert(useCase.get{}List_Called)\n".format(self.model_name)
			if self.is_sectioned_list:
				content += "        XCTAssertEqual({}??[0].{}List.count, 1)\n".format(list_name, self.model_variable)
			else:
				content += "        XCTAssertEqual({}??.count, 1)\n".format(list_name)
			content += "    }\n\n"
			content += "    func test_reloadTriggerInvoked_get{}List_failedShowError() {{\n".format(self.model_name)
			content += "        // arrange\n"
			content += "        let get{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
			content += "        useCase.get{}List_ReturnValue = get{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
			content += "        // act\n"
			content += "        reloadTrigger.onNext(())\n"
			content += "        get{}List_ReturnValue.onError(TestError())\n".format(self.model_name)
			content += "        let error = try? output.error.toBlocking(timeout: 1).first()\n\n"
			content += "        // assert\n"
			content += "        XCTAssert(useCase.get{}List_Called)\n".format(self.model_name)
			content += "        XCTAssert(error is TestError)\n"
			content += "    }\n\n"
			content += "    func test_reloadTriggerInvoked_notGet{}ListIfStillLoading() {{\n".format(self.model_name)
			content += "        // arrange\n"
			content += "        let get{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
			content += "        useCase.get{}List_ReturnValue = get{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
			content += "        // act\n"
			content += "        loadTrigger.onNext(())\n"
			content += "        useCase.get{}List_Called = false\n".format(self.model_name)
			content += "        reloadTrigger.onNext(())\n\n"
			content += "        // assert\n"
			content += "        XCTAssertFalse(useCase.get{}List_Called)\n".format(self.model_name)
			content += "    }\n\n"
			content += "    func test_reloadTriggerInvoked_notGet{}ListIfStillReloading() {{\n".format(self.model_name)
			content += "        // arrange\n"
			content += "        let get{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
			content += "        useCase.get{}List_ReturnValue = get{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
			content += "        // act\n"
			content += "        reloadTrigger.onNext(())\n"
			content += "        useCase.get{}List_Called = false\n".format(self.model_name)
			content += "        reloadTrigger.onNext(())\n\n"
			content += "        // assert\n"
			content += "        XCTAssertFalse(useCase.get{}List_Called)\n".format(self.model_name)
			content += "    }\n\n"
			content += "    func test_loadMoreTriggerInvoked_loadMore{}List() {{\n".format(self.model_name)
			content += "        // act\n"
			content += "        loadTrigger.onNext(())\n"
			content += "        loadMoreTrigger.onNext(())\n"
			content += "        let {} = try? output.{}.toBlocking(timeout: 1).first()\n\n".format(list_name, list_name)
			content += "        // assert\n"
			content += "        XCTAssert(useCase.loadMore{}List_Called)\n".format(self.model_name)
			if self.is_sectioned_list:
				content += "        XCTAssertEqual({}??[0].{}List.count, 2)\n".format(list_name, self.model_variable)
			else:
				content += "        XCTAssertEqual({}??.count, 2)\n".format(list_name)
			content += "    }\n\n"
			content += "    func test_loadMoreTriggerInvoked_loadMore{}List_failedShowError() {{\n".format(self.model_name)
			content += "        // arrange\n"
			content += "        let loadMore{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
			content += "        useCase.loadMore{}List_ReturnValue = loadMore{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
			content += "        // act\n"
			content += "        loadTrigger.onNext(())\n"
			content += "        loadMoreTrigger.onNext(())\n"
			content += "        loadMore{}List_ReturnValue.onError(TestError())\n".format(self.model_name)
			content += "        let error = try? output.error.toBlocking(timeout: 1).first()\n\n"
			content += "        // assert\n"
			content += "        XCTAssert(useCase.loadMore{}List_Called)\n".format(self.model_name)
			content += "        XCTAssert(error is TestError)\n"
			content += "    }\n\n"
			content += "    func test_loadMoreTriggerInvoked_notLoadMore{}ListIfStillLoading() {{\n".format(self.model_name)
			content += "        // arrange\n"
			content += "        let get{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
			content += "        useCase.get{}List_ReturnValue = get{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
			content += "        // act\n"
			content += "        loadTrigger.onNext(())\n"
			content += "        useCase.get{}List_Called = false\n".format(self.model_name)
			content += "        loadMoreTrigger.onNext(())\n\n"
			content += "        // assert\n"
			content += "        XCTAssertFalse(useCase.loadMore{}List_Called)\n".format(self.model_name)
			content += "    }\n\n"
			content += "    func test_loadMoreTriggerInvoked_notLoadMore{}ListIfStillReloading() {{\n".format(self.model_name)
			content += "        // arrange\n"
			content += "        let get{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
			content += "        useCase.get{}List_ReturnValue = get{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
			content += "        // act\n"
			content += "        reloadTrigger.onNext(())\n"
			content += "        useCase.get{}List_Called = false\n".format(self.model_name)
			content += "        loadMoreTrigger.onNext(())\n"
			content += "        // assert\n"
			content += "        XCTAssertFalse(useCase.loadMore{}List_Called)\n".format(self.model_name)
			content += "    }\n\n"
			content += "    func test_loadMoreTriggerInvoked_notLoadMoreDocumentTypesStillLoadingMore() {\n"
			content += "        // arrange\n"
			content += "        let loadMore{}List_ReturnValue = PublishSubject<PagingInfo<{}>>()\n".format(self.model_name, self.model_name)
			content += "        useCase.loadMore{}List_ReturnValue = loadMore{}List_ReturnValue\n\n".format(self.model_name, self.model_name)
			content += "        // act\n"
			content += "        loadMoreTrigger.onNext(())\n"
			content += "        useCase.loadMore{}List_Called = false\n".format(self.model_name)
			content += "        loadMoreTrigger.onNext(())\n\n"
			content += "        // assert\n"
			content += "        XCTAssertFalse(useCase.loadMore{}List_Called)\n".format(self.model_name)
			content += "    }\n\n"
			content += "    func test_select{}TriggerInvoked_to{}Detail() {{\n".format(self.model_name, self.model_name)
			content += "        // act\n"
			content += "        loadTrigger.onNext(())\n"
			content += "        select{}Trigger.onNext(IndexPath(row: 0, section: 0))\n\n".format(self.model_name)
			content += "        // assert\n"
			content += "        XCTAssert(navigator.to{}Detail_Called)\n".format(self.model_name)
			content += "    }\n"
			content += "}\n\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_use_case_mock(self):
			class_name = self.name + "UseCaseMock"
			content = self._file_header(class_name)
			content += "@testable import {}\n".format(self.project)
			content += "import RxSwift\n\n"
			content += "final class {0}: {1}UseCaseType {{\n\n".format(class_name, self.name)
			content += "    // MARK: - get{}List\n".format(self.model_name)
			content += "    var get{}List_Called = false\n".format(self.model_name)
			content += "    var get{}List_ReturnValue: Observable<PagingInfo<{}>> = {{\n".format(self.model_name, self.model_name)
			content += "        let items = [\n"
			content += "            {}().with {{ $0.id = 1 }}\n".format(self.model_name)
			content += "        ]\n"
			content += "        let page = PagingInfo<{}>(page: 1, items: OrderedSet(sequence: items))\n".format(self.model_name)
			content += "        return Observable.just(page)\n"
			content += "    }()\n"
			content += "    func get{}List() -> Observable<PagingInfo<{}>> {{\n".format(self.model_name, self.model_name)
			content += "        get{}List_Called = true\n".format(self.model_name)
			content += "        return get{}List_ReturnValue\n".format(self.model_name)
			content += "    }\n\n"
			content += "    // MARK: - loadMore{}List\n".format(self.model_name)
			content += "    var loadMore{}List_Called = false\n".format(self.model_name)
			content += "    var loadMore{}List_ReturnValue: Observable<PagingInfo<{}>> = {{\n".format(self.model_name, self.model_name)
			content += "        let items = [\n"
			content += "            {}().with {{ $0.id = 2 }}\n".format(self.model_name)
			content += "        ]\n"
			content += "        let page = PagingInfo<{}>(page: 2, items: OrderedSet(sequence: items))\n".format(self.model_name)
			content += "        return Observable.just(page)\n"
			content += "    }()\n"
			content += "    func loadMore{}List(page: Int) -> Observable<PagingInfo<{}>> {{\n".format(self.model_name, self.model_name)
			content += "        loadMore{}List_Called = true\n".format(self.model_name)
			content += "        return loadMore{}List_ReturnValue\n".format(self.model_name)
			content += "    }\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_navigator_mock(self):
			class_name = self.name + "NavigatorMock"
			content = self._file_header(class_name)
			content += "@testable import {}\n\n".format(self.project)
			content += "final class {0}: {1}NavigatorType {{\n\n".format(class_name, self.name)
			content += "    // MARK: - to{}\n".format(self.name)
			content += "    var to{}_Called = false\n".format(self.name)
			content += "    func to{}() {{\n".format(self.name)
			content += "        to{}_Called = true\n".format(self.name)
			content += "    }\n\n"
			content += "    // MARK: - to{}Detail\n".format(self.model_name)
			content += "    var to{}Detail_Called = false\n".format(self.model_name)
			content += "    func to{}Detail({}: {}) {{\n".format(self.model_name, self.model_variable, self.model_name)
			content += "        to{}Detail_Called = true\n".format(self.model_name)
			content += "    }\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_view_controller_tests(self):
			class_name = self.name + "ViewControllerTests"
			content = self._file_header(class_name)
			content += "@testable import {}\n".format(self.project)
			content += "import XCTest\nimport Reusable\n\n"
			content += "final class {0}: XCTestCase {{\n\n".format(class_name)
			content += "    private var viewController: {}ViewController!\n\n".format(self.name)
			content += "    override func setUp() {\n		super.setUp()\n"
			content += "//        viewController = {}ViewController.instantiate()\n	}}\n\n".format(self.name)
			content += "    func test_ibOutlets() {\n"
			content += "//        _ = viewController.view\n"
			content += "//        XCTAssertNotNil(viewController.tableView)\n"
			content += "    }\n}\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_table_view_cell_tests(self):
			class_name = "{}CellTests".format(self.model_name)
			content = self._file_header(class_name)
			content += "import XCTest\n"
			content += "@testable import {}\n\n".format(self.project)
			content += "final class {}: XCTestCase {{\n".format(class_name)
			content += "    var cell: {}Cell!\n\n".format(self.model_name)
			content += "    override func setUp() {\n"
			content += "        super.setUp()\n"
			content += "//        cell = {}Cell.loadFromNib()\n".format(self.model_name)
			content += "    }\n\n"
			content += "    func test_iboutlets() {\n"
			content += "//        XCTAssertNotNil(cell)\n"
			for p in self.model.properties:
				if p.name != "id":
					if p.is_url:
						content += "//        XCTAssertNotNil(cell.{}ImageView)\n".format(p.name)
					else:
						content += "//        XCTAssertNotNil(cell.{}Label)\n".format(p.name)
			content += "    }\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)


	#=================== DetailTemplate ===================


	class DetailTemplate(BaseTemplate):
		def __init__(self, model, options, name, project, developer, company, date):
			super(Template.DetailTemplate, self).__init__(name, project, developer, company, date)
			self.model = model
			self.options = options
			self.model_name = self.model.name
			self.model_variable = camel_case(self.model_name)

		def create_files(self):
			print(" ")
			self._make_dirs()
			self._create_view_model()
			self._create_navigator()
			self._create_use_case()
			self._create_view_controller()
			self._create_cells()
			self._create_view_model_tests()
			self._create_use_case_mock()
			self._create_navigator_mock()
			self._create_view_controller_tests()
			self._create_cells_tests()
			print(" ")

		def _create_view_model(self):
			class_name = self.name + "ViewModel"
			content = self._file_header(class_name)
			content += "struct {0}: ViewModelType {{\n\n".format(class_name)
			content += "    struct Input {\n"
			content += "        let loadTrigger: Driver<Void>\n"
			content += "    }\n\n"
			content += "    struct Output {\n"
			content += "        let cells: Driver<[CellType]>\n"
			content += "    }\n\n"
			content += "    enum CellType {\n"
			for p in self.model.properties:
				if p.name != "id":
					content += "        case {}({})\n".format(p.name, p.type.name)
			content += "    }\n\n"
			content += "    let navigator: {}NavigatorType\n".format(self.name)
			content += "    let useCase: {}UseCaseType\n".format(self.name)
			content += "    let {}: {}\n\n".format(self.model_variable, self.model_name)
			content += "    func transform(_ input: Input) -> Output {\n"
			content += "        let {} = input.loadTrigger\n".format(self.model_variable)
			content += "            .map {{ self.{} }}\n".format(self.model_variable)
			content += "        let cells = {}\n".format(self.model_variable)
			content += "            .map {{ {} -> [CellType] in\n".format(self.model_variable)
			content += "                var cells = [CellType]()\n"
			for p in self.model.properties:
				if p.name != "id":
					content += "                cells.append(CellType.{}({}.{}))\n".format(p.name, self.model_variable, p.name)
			content += "                return cells\n"
			content += "            }\n"
			content += "        return Output(cells: cells)\n"
			content += "    }\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_navigator(self):
			class_name = self.name + "Navigator"
			protocol_name = class_name + "Type"
			content = self._file_header(class_name)
			content += "protocol {}NavigatorType {{\n".format(self.name)
			content += "    func to{}({}: {})\n".format(self.name, self.model_variable, self.model_name)
			content += "}\n\n"
			content += "struct {}Navigator: {}NavigatorType {{\n".format(self.name, self.name)
			content += "    unowned let navigationController: UINavigationController\n\n"
			content += "    func to{}({}: {}) {{\n".format(self.name, self.model_variable, self.model_name)
			content += "        let useCase = {}UseCase()\n".format(self.name)
			content += "        let vm = {}ViewModel(navigator: self, useCase: useCase, {}: {})\n".format(self.name, self.model_variable, self.model_variable)
			content += "        let vc = {}ViewController.instantiate()\n".format(self.name)
			content += "        vc.bindViewModel(to: vm)\n"
			content += "        navigationController.pushViewController(vc, animated: true)\n"
			content += "    }\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_view_controller(self):
			class_name = self.name + "ViewController"
			content = self._file_header(class_name)
			content += "import UIKit\nimport Reusable\n\n"
			content += "final class {}: UIViewController, BindableType {{\n\n".format(class_name)
			content += "    @IBOutlet weak var tableView: UITableView!\n"
			content += "    var viewModel: {}ViewModel!\n\n".format(self.name)
			content += "    override func viewDidLoad() {\n"
			content += "        super.viewDidLoad()\n"
			content += "        configView()\n"
			content += "    }\n\n"
			content += "    private func configView() {\n"
			content += "        tableView.do {\n"
			content += "            $0.estimatedRowHeight = 550\n"
			content += "            $0.rowHeight = UITableViewAutomaticDimension\n"
			for p in self.model.properties:
				if p.name != "id":
					content += "            $0.register(cellType: {}{}Cell.self)\n".format(self.model_name, p.name_title)
			content += "        }\n"
			content += "    }\n"
			content += "    deinit {\n"
			content += "        logDeinit()\n"
			content += "    }\n\n"
			content += "    func bindViewModel() {\n"
			content += "        let input = {}ViewModel.Input(loadTrigger: Driver.just(()))\n".format(self.name)
			content += "        let output = viewModel.transform(input)\n"
			content += "        output.cells\n"
			content += "            .drive(tableView.rx.items) { tableView, index, cellType in\n"
			content += "                let indexPath = IndexPath(row: index, section: 0)\n"
			content += "                switch cellType {\n"
			for p in self.model.properties:
				if p.name != "id":
					content += "                case let .{}({}):\n".format(p.name, p.name)
					content += "                    return tableView.dequeueReusableCell(\n"
					content += "                        for: indexPath,\n"
					content += "                        cellType: {}{}Cell.self)\n".format(self.model_name, p.name_title)
			content += "                }\n"
			content += "            }\n"
			content += "            .disposed(by: rx.disposeBag)\n"
			content += "    }\n\n}\n\n"
			content += "// MARK: - StoryboardSceneBased\n"
			content += "extension {}ViewController: StoryboardSceneBased {{\n".format(self.name)
			content += "    // TODO: - Update storyboard\n"
			content += "    static var sceneStoryboard = UIStoryboard()\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_cells(self):
			for p in self.model.properties:
				if p.name != "id":
					self._create_cell(p)

		def _create_cell(self, property):
			class_name = "{}{}Cell".format(self.model_name, property.name_title)
			content = self._file_header(class_name)
			content += "import UIKit\nimport Reusable\n\n"
			content += "final class {}{}Cell: UITableViewCell, NibReusable {{\n".format(self.model_name, property.name_title)
			if property.is_url:
				content += "    @IBOutlet weak var {}ImageView: UIImageView!\n".format(property.name)
			else:
				content += "    @IBOutlet weak var {}Label: UILabel!\n".format(property.name)
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_view_model_tests(self):
			class_name = self.name + "ViewModelTests"
			content = self._file_header(class_name)
			content += "@testable import {}\n".format(self.project)
			content += "import XCTest\nimport RxSwift\nimport RxBlocking\n\n"
			content += "final class {}ViewModelTests: XCTestCase {{\n\n".format(self.name)
			content += "    private var viewModel: {}ViewModel!\n".format(self.name)
			content += "    private var navigator: {}NavigatorMock!\n".format(self.name)
			content += "    private var useCase: {}UseCaseMock!\n".format(self.name)
			content += "    private var disposeBag: DisposeBag!\n"
			content += "    private var input: {}ViewModel.Input!\n".format(self.name)
			content += "    private var output: {}ViewModel.Output!\n".format(self.name)
			content += "    private let loadTrigger = PublishSubject<Void>()\n\n"
			content += "    override func setUp() {\n"
			content += "        super.setUp()\n"
			content += "        navigator = {}NavigatorMock()\n".format(self.name)
			content += "        useCase = {}UseCaseMock()\n".format(self.name)
			content += "        viewModel = {}ViewModel(navigator: navigator, useCase: useCase, {}: {}())\n".format(self.name, self.model_variable, self.model_name)
			content += "        disposeBag = DisposeBag()\n"
			content += "        input = {}ViewModel.Input(\n".format(self.name)
			content += "            loadTrigger: loadTrigger.asDriverOnErrorJustComplete()\n"
			content += "        )\n"
			content += "        output = viewModel.transform(input)\n"
			content += "        output.cells.drive().disposed(by: disposeBag)\n"
			content += "    }\n\n"
			content += "    func test_loadTriggerInvoked_createCells() {\n"
			content += "        // act\n"
			content += "        loadTrigger.onNext(())\n"
			content += "        let cells = try? output.cells.toBlocking(timeout: 1).first()\n\n"
			content += "        // assert\n"
			content += "        XCTAssertNotEqual(cells??.count, 0)\n"
			content += "    }\n\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_navigator_mock(self):
			class_name = self.name + "NavigatorMock"
			content = self._file_header(class_name)
			content += "@testable import {}\n\n".format(self.project)
			content += "final class {}NavigatorMock: {}NavigatorType {{\n".format(self.name, self.name)
			content += "    func to{}({}: {}) {{\n\n".format(self.name, self.model_variable, self.model_name)
			content += "    }\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_view_controller_tests(self):
			class_name = self.name + "ViewControllerTests"
			content = self._file_header(class_name)
			content += "@testable import {}\n".format(self.project)
			content += "import XCTest\nimport Reusable\n\n"
			content += "final class {0}: XCTestCase {{\n\n".format(class_name)
			content += "    private var viewController: {}ViewController!\n\n".format(self.name)
			content += "    override func setUp() {\n"
			content += "        super.setUp()\n"
			content += "        viewController = {}ViewController.instantiate()\n".format(self.name)
			content += "    }\n\n"
			content += "    func test_ibOutlets() {\n"
			content += "        _ = viewController.view\n"
			content += "        XCTAssertNotNil(viewController.tableView)\n"
			content += "    }\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_cells_tests(self):
			class_name = "{}CellsTests".format(self.name)
			content = self._file_header(class_name)
			content += "@testable import {}\n".format(self.project)
			content += "import XCTest\n\n"
			content += "final class {0}: XCTestCase {{\n\n".format(class_name)
			for p in self.model.properties:
				if p.name != "id":
					content += "    private var {}Cell: {}{}Cell!\n".format(p.name, self.model_name, p.name_title)
			content += "\n"
			content += "    override func setUp() {\n"
			content += "        super.setUp()\n"
			for p in self.model.properties:
				if p.name != "id":
					content += "        {}Cell = {}{}Cell.loadFromNib()\n".format(p.name, self.model_name, p.name_title)
			content += "    }\n\n"
			content += "    func test_iboutlets() {\n"
			for p in self.model.properties:
				if p.name != "id":
					content += "        XCTAssertNotNil({}Cell.{}Label)\n".format(p.name, p.name)
			content += "    }\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)


	#=================== StaticDetailTemplate ===================


	class StaticDetailTemplate(DetailTemplate):

		def create_files(self):
			print(" ")
			self._make_dirs()
			self._create_view_model()
			self._create_navigator()
			self._create_use_case()
			self._create_view_controller()
			self._create_view_model_tests()
			self._create_use_case_mock()
			self._create_navigator_mock()
			self._create_view_controller_tests()
			self._create_cells_tests()
			print(" ")

		def _create_view_model(self):
			class_name = self.name + "ViewModel"
			content = self._file_header(class_name)
			content += "struct {}ViewModel: ViewModelType {{\n\n".format(self.name)
			content += "    struct Input {\n"
			content += "        let loadTrigger: Driver<Void>\n"
			content += "    }\n\n"
			content += "    struct Output {\n"
			content += "        let name: Driver<String>\n"
			content += "        let price: Driver<Double>\n"
			content += "    }\n\n"
			content += "    let navigator: {}NavigatorType\n".format(self.name)
			content += "    let useCase: {}UseCaseType\n".format(self.name)
			content += "    let {}: {}\n\n".format(self.model_variable, self.model_name)
			content += "    func transform(_ input: Input) -> Output {\n"
			content += "        let {} = input.loadTrigger\n".format(self.model_variable)
			content += "            .map {{ self.{} }}\n".format(self.model_variable)
			for p in self.model.properties:
				if p.name != "id":
					content += "        let {} = {}.map {{ $0.{} }}\n".format(p.name, self.model_variable, p.name)
			outputs = []
			for p in self.model.properties:
				if p.name != "id":
					output = "            {}: {}".format(p.name, p.name)
					outputs.append(output)
			content += "        return Output(\n"
			content += ",\n".join(outputs)
			content += "\n"
			content += "        )\n"
			content += "    }\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_view_controller(self):
			class_name = self.name + "ViewController"
			content = self._file_header(class_name)
			content += "import UIKit\nimport Reusable\n\n"
			content += "final class {}ViewController: UITableViewController, BindableType {{\n\n".format(self.name)
			for p in self.model.properties:
				if p.name != "id":
					if p.is_url:
						content += "    @IBOutlet weak var {}ImageView: UIImageView!\n".format(p.name)
					else:
						content += "    @IBOutlet weak var {}Label: UILabel!\n".format(p.name)
			content += "\n"
			content += "    var viewModel: {}ViewModel!\n\n".format(self.name)
			content += "    override func viewDidLoad() {\n"
			content += "        super.viewDidLoad()\n"
			content += "    }\n\n"
			content += "    deinit {\n"
			content += "        logDeinit()\n"
			content += "    }\n\n"
			content += "    func bindViewModel() {\n"
			content += "        let input = {}ViewModel.Input(\n".format(self.name)
			content += "            loadTrigger: Driver.just(())\n"
			content += "        )\n"
			content += "        let output = viewModel.transform(input)\n"
			for p in self.model.properties:
				if p.name != "id":
					content += "        output.{}\n".format(p.name)
					content += "            .drive()\n"
					content += "            .disposed(by: rx.disposeBag)\n"
			content += "    }\n"
			content += "}\n"
			content += "// MARK: - StoryboardSceneBased\n"
			content += "extension {}ViewController: StoryboardSceneBased {{\n".format(self.name)
			content += "    // TODO: - Update storyboard\n"
			content += "    static var sceneStoryboard = UIStoryboard()\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_view_model_tests(self):
			class_name = self.name + "ViewModelTests"
			content = self._file_header(class_name)
			content += "@testable import {}\n".format(self.project)
			content += "import XCTest\nimport RxSwift\nimport RxBlocking\n\n"
			content += "final class {}ViewModelTests: XCTestCase {{\n\n".format(self.name)
			content += "    private var viewModel: {}ViewModel!\n".format(self.name)
			content += "    private var navigator: {}NavigatorMock!\n".format(self.name)
			content += "    private var useCase: {}UseCaseMock!\n".format(self.name)
			content += "    private var disposeBag: DisposeBag!\n"
			content += "    private var input: {}ViewModel.Input!\n".format(self.name)
			content += "    private var output: {}ViewModel.Output!\n".format(self.name)
			content += "    private let loadTrigger = PublishSubject<Void>()\n\n"
			content += "    override func setUp() {\n"
			content += "        super.setUp()\n"
			content += "        navigator = {}NavigatorMock()\n".format(self.name)
			content += "        useCase = {}UseCaseMock()\n".format(self.name)
			content += "        viewModel = {}ViewModel(navigator: navigator, useCase: useCase, {}: {}())\n".format(self.name, self.model_variable, self.model_name)
			content += "        disposeBag = DisposeBag()\n"
			content += "        input = {}ViewModel.Input(\n".format(self.name)
			content += "            loadTrigger: loadTrigger.asDriverOnErrorJustComplete()\n"
			content += "        )\n"
			content += "        output = viewModel.transform(input)\n"
			for p in self.model.properties:
				if p.name != "id":
					content += "        output.{}.drive().disposed(by: disposeBag)\n".format(p.name)
			content += "    }\n\n"
			content += "    func test_loadTriggerInvoked_createCells() {\n"
			content += "        // act\n"
			content += "        loadTrigger.onNext(())\n"
			for p in self.model.properties:
				if p.name != "id":
					content += "        let {} = try? output.{}.toBlocking(timeout: 1).first()\n".format(p.name, p.name)
			content += "\n"
			content += "        // assert\n"
			content += "        XCTAssert(true)\n"
			content += "    }\n\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)

		def _create_view_controller_tests(self):
			class_name = self.name + "ViewControllerTests"
			content = self._file_header(class_name)
			content += "@testable import {}\n".format(self.project)
			content += "import XCTest\nimport Reusable\n\n"
			content += "final class {0}: XCTestCase {{\n\n".format(class_name)
			content += "    private var viewController: {}ViewController!\n\n".format(self.name)
			content += "    override func setUp() {\n"
			content += "        super.setUp()\n"
			content += "        viewController = {}ViewController.instantiate()\n".format(self.name)
			content += "    }\n\n"
			content += "    func test_ibOutlets() {\n"
			content += "        _ = viewController.view\n"
			content += "        XCTAssertNotNil(viewController.tableView)\n"
			for p in self.model.properties:
				if p.name != "id":
					if p.is_url:
						content += "        XCTAssertNotNil(viewController.{}ImageView)\n".format(p.name)
					else:
						content += "        XCTAssertNotNil(viewController.{}Label)\n".format(p.name)
			content += "    }\n"
			content += "}\n"
			file_name = class_name + ".swift"
			file_path = "{}/Test/{}.swift".format(self.name, class_name)
			self._create_file(file_path, file_name, content)


#=================== JSON ===================


class JSON(object):
	JSON_TO_SWIFT_TYPES = { 
		"int": "Int",
		"bool": "Bool",
		"unicode": "String",
		"float": "Double",
		"NoneType": "Any?"
	}

	SWIFT_TYPES_DEFAULT_VALUES = {
		"Int": "0",
		"Bool": "false",
		"String": '""',
		"Double": "0.0",
		"Date": "Date()"
	}

	SWIFT_TYPES = { "Int", "Bool", "String", "Double", "Date", "Any" }

	DATE_REGEX = r"(\d{4})[-/](\d{2})[-/](\d{2})"

	class Property(object):
		def __init__(self, raw_name, name, type_name):
			self.raw_name = raw_name
			self.name = name
			self.type_name = type_name

		def is_user_type(self):
			return self.type_name.endswith("?") and self.original_type_name() not in JSON.SWIFT_TYPES

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
			for p in self.properties:
				if p.type_name.endswith("?"):
					if p.original_type_name() in JSON.SWIFT_TYPES:
						content += "            {}: nil\n".format(p.name)
				else:
					if p.type_name in JSON.SWIFT_TYPES_DEFAULT_VALUES:
						default_value = JSON.SWIFT_TYPES_DEFAULT_VALUES[p.type_name]
					else:
						default_value = "{}()".format(p.type_name)
					content += "            {}: {}\n".format(p.name, default_value)
			content += "        )\n"
			content += "    }\n"
			content += "}\n\n"
			content += "extension {}: Then {{ }}\n\n".format(self.name)
			content += "extension {}: Mappable {{\n\n".format(self.name)
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
				var_type = "[{}]?".format(singular_var_name.title())
				if len(value) > 0:
					self._extract_model(singular_var_name.title(), value[0], models)
				else:
					var_type = "[Any]?"
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

	DEFAULT_VALUES = {
		"Int": "0",
		"Bool": "false",
		"String": '""',
		"Double": "0.0",
		"Float": "0.0",
		"Date": "Date()"
	}

	SYSTEM_TYPES = { "Int", "Bool", "String", "Double", "Float", "Date" }

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
		content = "final class {}Mock: {} {{\n\n".format(class_name, protocol_name)
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
			elif f.return_type in Mock.SYSTEM_TYPES:
				return_value = Mock.DEFAULT_VALUES[f.return_type]
			else:
				return_value = "{}()".format(f.return_type)
			if f.return_type != None:
				content += "    var {}_ReturnValue: {} = {}\n".format(f.name, f.return_type, return_value)
			content += "\n"
			content += "    {} {{\n".format(f.origin)
			content += "        {}_Called = true\n".format(f.name)
			if f.return_type != None:
				content += "        return {}_ReturnValue\n".format(f.name)
			content += "    }\n\n"
		content += "}\n"
		return content

#=================== Mock ===================

class API(object):
	def __init__(self, api_name):
		super(API, self).__init__()
		self.api_name = api_name

	def create_api(self):
		name = self.api_name
		content = "// MARK: - {}\n".format(name)
		content += "extension API {\n"
		content += "    func {}(_ input: {}Input) -> Observable<{}Output> {{\n".format(camel_case(name), name, name)
		content += "        return request(input)\n"
		content += "    }\n\n"
		content += "    final class {}Input: APIInput {{\n".format(name)
		content += "        init() {\n"
		content += "            super.init(urlString: API.Urls.{},\n".format(camel_case(name))
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

		content = "final class {}ViewModelTests: XCTestCase {{\n\n".format(view_model)
		content += "    private var viewModel: {}ViewModel!\n".format(view_model)
		content += "    private var navigator: {}NavigatorMock!\n".format(view_model)
		content += "    private var useCase: {}UseCaseMock!\n".format(view_model)
		content += "    private var disposeBag: DisposeBag!\n\n"
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
			content += "    func test_{}Invoked_() {{\n".format(p.name)
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

	def __init__(self, model_text):
		super(Model, self).__init__()
		self.model_text = model_text

class InitModel(Model):

	def create_init(self):
		pass


#=================== Commands ===================

class Commmands:
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
		help = "iTools commands:\n"
		help += format("   help", "<15") + "Show help\n"
		help += format("   header", "<15") + "Update file header info\n"
		help += format("   template", "<15") + "Generate template files\n"
		help += format("   json", "<15") + "Create models from json text\n"
		help += format("   mock", "<15") + "Create mock from protocol\n"
		help += format("   api", "<15") + "Create API request\n"
		help += format("   test", "<15") + "Create Unit Tests from view model\n"
		help += format("   bind", "<15") + "Create bindViewModel method for view controller from view model\n"
		help += format("   init", "<15") + "Create init method for model\n"
		help += "\n"
		help += "Get help on a command: python it.py help [command]\n"
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
				model = Template()._parse_model(model_text)
				template = Template.ListTemplate(model, self.options, self.scene_name, project, developer, company, date)
				template.create_files()
				print("Finish!")
			except:
				print('Invalid model text in clipboard.')
		elif self.template_name == Template.TemplateType.DETAIL:
			model_text = pasteboard_read()
			try:
				model = Template()._parse_model(model_text)
				if "--static" in self.options:
					template = Template.StaticDetailTemplate(model, self.options, self.scene_name, project, developer, company, date)
				else:
					template = Template.DetailTemplate(model, self.options, self.scene_name, project, developer, company, date)
				template.create_files()
				print("Finish!")
			except:
				print('Invalid model text in clipboard.')
		else:
			print("Invalid template name.")


class JSONCommand(object):
	def __init__(self, model_name, json_text):
		super(JSONCommand, self).__init__()
		self.model_name = model_name
		self.json_text = json_text

	def create_models(self):
		try:
			output = JSON(self.model_name, self.json_text).create_models()
			pasteboard_write(output)
			print("Text has been copied to clipboard.")
		except:
			print("Invalid json string in clipboard.")


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

	def create_tests(self):
		try:
			output = BindViewModel(self.vm_text).create_bind_view_model()
			pasteboard_write(output)
			print("Text has been copied to clipboard.")
		except:
			print("Invalid view model text in clipboard.")		

#=================== Main ===================


def execute(args):
	command = args[0]
	if command == "t":
		command = "template"
	if command == Commmands.HELP:
		HelpCommand().show_help()
	elif command == Commmands.HEADER:
		FileHeaderCommand().update_file_header()
	elif command == Commmands.TEMPLATE:
		if len(args) >= 3:
			template_name = args[1]
			scene_name = args[2]
			options = args[3:]
			TemplateCommmand(template_name, scene_name, options).create_files()
		else:
			print("Invalid params.")
	elif command == Commmands.JSON:
		if len(args) >= 2:
			model_name = args[1]
			json = pasteboard_read()
			JSONCommand(model_name, json).create_models()
		else:
			print("Missing model name.")
	elif command == Commmands.MOCK:
		protocol_text = pasteboard_read()
		MockCommand(protocol_text).create_mock()
	elif command == Commmands.API:
		if len(args) >= 2:
			api_name = args[1]
			APICommand(api_name).create_api()
		else:
			print("Missing api name.")
	elif command == Commmands.UNIT_TEST:
		vm_text = pasteboard_read()
		UnitTestCommand(vm_text).create_tests()
	elif command == Commmands.BIND_VIEW_MODEL:
		vm_text = pasteboard_read()
		BindViewModelCommand(vm_text).create_tests()
	elif command == Commands.INIT:
		pass
	else:
		print("'{}' is not a valid command. See 'python it.py help'.".format(command))

if len(sys.argv) > 1:
	execute(sys.argv[1:])
else:
	HelpCommand().show_help()




