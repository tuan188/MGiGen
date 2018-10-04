# coding=utf-8

import sys
from .str_helpers import lower_first_letter, upper_first_letter, snake_to_camel, plural_to_singular
from .constants import Commands, FILE_HEADER, SWIFT_TYPES_DEFAULT_VALUES, SWIFT_TYPES
from .pb import pasteboard_read, pasteboard_write

from .init_cmd import InitCommand
from .bind_cmd import BindViewModelCommand
from .test_cmd import UnitTestCommand
from .api_cmd import APICommand
from .mock_cmd import MockCommand
from .json_cmd import JSONCommand
from .help_cmd import HelpCommand
from .header_cmd import FileHeaderCommand
from .template_cmd import TemplateCommand


def execute(args):
	command = args[0]
	if command == "t":
		command = "template"
	if command == Commands.HELP:
		if len(args) >= 2:
			command_name = args[1]
			HelpCommand().show_help_for(command_name)
		else:
			HelpCommand().show_help()
	elif command == Commands.HEADER:
		FileHeaderCommand().update_file_header()
	elif command == Commands.TEMPLATE:
		if len(args) >= 3:
			template_name = args[1]
			scene_name = args[2]
			options = args[3:]
			TemplateCommand(template_name, scene_name, options).create_files()
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



