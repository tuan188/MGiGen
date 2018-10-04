# coding=utf-8

from .command import Command
from .init_cmd import InitCommand
from .bind_cmd import BindViewModelCommand
from .test_cmd import UnitTestCommand
from .api_cmd import APICommand
from .mock_cmd import MockCommand
from .json_cmd import JSONCommand
from .header_cmd import FileHeaderCommand
from .template_cmd import TemplateCommand


class HelpCommand(Command):

	@classmethod
	def description(cls):
		return "Show help"

	@classmethod
	def name(cls):
		return "help"
		
	def show_help(self):
		help = "igen commands:\n\n"
		commands = "\n".join([
			HelpCommand.long_description(),
			FileHeaderCommand.long_description(),
			TemplateCommand.long_description(),
			JSONCommand.long_description(),
			MockCommand.long_description(),
			APICommand.long_description(),
			UnitTestCommand.long_description(),
			BindViewModelCommand.long_description(),
			InitCommand.long_description()
		])
		help += commands
		help += "\n\n"
		help += "Get help on a command: igen help [command]\n"
		print(help)


	
	