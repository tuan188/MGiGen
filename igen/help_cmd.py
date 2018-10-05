# coding=utf-8

from collections import OrderedDict
from . import __version__
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

	def __init__(self):
		super(HelpCommand, self).__init__()
		self.commands = dict((eval(cmd).name(), eval(cmd).class_name()) for cmd in COMMANDS)

	@classmethod
	def description(cls):
		return "Show help"

	@classmethod
	def name(cls):
		return "help"
		
	def show_help(self):
		help = "igen v" + __version__ + "\n"
		help += "Commands:\n\n"
		help += "\n".join([eval(cmd).long_description() for cmd in COMMANDS])
		help += "\n\n"
		help += "Get help on a command: igen help [command]\n"
		print(help)

	def show_help_for(self, command):
		commandNames = [eval(cmd).name() for cmd in COMMANDS]
		if command in commandNames:
			cmd = eval(self.commands[command])
			print(cmd.help())
		else:
			HelpCommand.help()


COMMANDS = [
		HelpCommand.class_name(),
		FileHeaderCommand.class_name(),
		TemplateCommand.class_name(),
		JSONCommand.class_name(),
		MockCommand.class_name(),
		APICommand.class_name(),
		UnitTestCommand.class_name(),
		BindViewModelCommand.class_name(),
		InitCommand.class_name()
	]