# coding=utf-8

import sys
from StringHelpers import lower_first_letter, upper_first_letter, snake_to_camel, plural_to_singular
from Constants import Commands
from InitCommand import InitCommand
from Constants import FILE_HEADER, SWIFT_TYPES_DEFAULT_VALUES, SWIFT_TYPES
from Pasteboard import pasteboard_read, pasteboard_write
from BindViewModelCommand import BindViewModelCommand
from UnitTestCommand import UnitTestCommand
from APICommand import APICommand
from MockCommand import MockCommand
from JSONCommand import JSONCommand
from HelpCommand import HelpCommand
from FileHeaderCommand import FileHeaderCommand
from TemplateCommmand import TemplateCommmand


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
		print("'{}' is not a valid command. See 'igen help'.".format(command))



