# coding=utf-8

import re
from jinja2 import Environment, PackageLoader

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