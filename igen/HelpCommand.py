# coding=utf-8

from Command import Command
from InitCommand import InitCommand
from BindViewModelCommand import BindViewModelCommand
from UnitTestCommand import UnitTestCommand
from APICommand import APICommand
from MockCommand import MockCommand
from JSONCommand import JSONCommand
from FileHeaderCommand import FileHeaderCommand
from TemplateCommand import TemplateCommand


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


	
	