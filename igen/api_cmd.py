# coding=utf-8

from jinja2 import Environment, PackageLoader
from .str_helpers import lower_first_letter, upper_first_letter
from .pb import pasteboard_write
from .command import Command

class APICommand(Command):
	def __init__(self, api_name):
		super(APICommand, self).__init__()
		self.api_name = api_name

	def create_api(self, print_result):
		output = API(self.api_name).create_api()
		if print_result:
			print()
			print(output)
			print()
		pasteboard_write(output)
		print('The result has been copied to the pasteboard.')


class API(object):
	def __init__(self, api_name):
		super(API, self).__init__()
		self.api_name = api_name
		self.env = Environment(
			loader=PackageLoader('igen_templates', 'commands'),
			trim_blocks=True,
			lstrip_blocks=True
		)

	def create_api(self):
		name = upper_first_letter(self.api_name)
		var_name = lower_first_letter(name)
		template = self.env.get_template("API.swift")
		content = template.render(
			name=name,
			var_name=var_name
		)
		return content