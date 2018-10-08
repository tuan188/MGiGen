import sys
import argparse
from arghandler import *

from . import __version__
from .pb import pasteboard_read
from .api_cmd import APICommand
from .mock_cmd import MockCommand
from .init_cmd import InitCommand
from .config_cmd import ConfigCommand
from .json_cmd import JSONCommand
from .test_cmd import UnitTestCommand
from .bind_cmd import BindViewModelCommand
from .template_cmd import TemplateCommand

@subcmd('template', help='create template files for the scene')
def cmd_template(parser, context, args):
	parser.epilog="'list' and 'detail' template require copying the Model to the pasteboard before running the command."
	parser.description='Create template files for the scene.'
	parser.add_argument(
		'type',
		nargs=1,
		choices=['base', 'list', 'detail'],
		help="template type"
	)
	parser.add_argument(
		'name',
		nargs=1,
		help='scene name'
	)
	parser.add_argument(
		'--section', 
		required=False,
		action='store_true',
		help="show a list of items with header sections ('list' template only)"
	)
	parser.add_argument(
		'--collection', 
		required=False, 
		action='store_true', 
		help="use UICollectionView instead of UITableView ('list' template only)"
	)
	parser.add_argument(
		'--static', 
		required=False, 
		action='store_true', 
		help="display details in a static UITableViewController ('detail' template only)"
	)
	args = parser.parse_args(args)
	template_name = args.type[0]
	scene_name = args.name[0]
	options = {
		'section': args.section,
		'collection': args.collection,
		'static': args.static,
	}
	TemplateCommand(template_name, scene_name, options).create_files()


@subcmd('mock', help='create mock for the protocol')
def cmd_mock(parser, context, args):
	parser.usage = 'copy the protocol to the pasteboard then run: igen mock [-h] [-p]'
	parser.description='Create mock for the protocol.'
	parser.add_argument(
		'-p', '--print', 
		required=False, 
		action='store_true', 
		help="print the result"
	)
	args = parser.parse_args(args)
	protocol_text = pasteboard_read()
	MockCommand(protocol_text).create_mock(args.print)


@subcmd('test', help='create unit tests for the ViewModel')
def cmd_test(parser, context, args):
	parser.usage = 'copy the ViewModel to the pasteboard then run: igen test [-h] [-p]'
	parser.description='Create unit tests for the ViewModel.'
	parser.add_argument(
		'-p', '--print', 
		required=False, 
		action='store_true', 
		help="print the result"
	)
	args = parser.parse_args(args)
	vm_text = pasteboard_read()
	UnitTestCommand(vm_text).create_tests(args.print)


@subcmd('bind', help='create bindViewModel method for the UIViewController')
def cmd_test(parser, context, args):
	parser.usage = 'copy the ViewModel to the pasteboard then run: igen bind [-h] [-p]'
	parser.description='Create bindViewModel method for the UIViewController.'
	parser.add_argument(
		'-p', '--print', 
		required=False, 
		action='store_true', 
		help="print the result"
	)
	args = parser.parse_args(args)
	vm_text = pasteboard_read()
	BindViewModelCommand(vm_text).create_bind_view_model(args.print)


@subcmd('init', help='create initialize method for the class/struct')
def cmd_init(parser, context, args):
	parser.usage = 'copy the protocol to the pasteboard then run: igen init [-h] [-p]'
	parser.description='Create initialize method for the class/struct.'
	parser.add_argument(
		'-p', '--print', 
		required=False, 
		action='store_true', 
		help="print the result"
	)
	args = parser.parse_args(args)
	model_text = pasteboard_read()
	InitCommand(model_text).create_init(args.print)


@subcmd('json', help='create model from JSON')
def cmd_json(parser, context, args):
	parser.usage = 'copy the JSON to the pasteboard then run: igen json [-h] [-p] name'
	parser.description='Create model from JSON.'
	parser.add_argument(
		'name',
		nargs=1,
		help='model name'
	)
	parser.add_argument(
		'-p', '--print', 
		required=False, 
		action='store_true', 
		help="print the result"
	)
	args = parser.parse_args(args)
	json = pasteboard_read()
	JSONCommand(args.name[0], json).create_models(args.print)


@subcmd('api', help='create input and ouput files for the API')
def cmd_api(parser, context, args):
	parser.description='Create input and ouput files for the API.'
	parser.add_argument(
		'name',
		nargs=1,
		help='api name'
	)
	parser.add_argument(
		'-p', '--print', 
		required=False, 
		action='store_true', 
		help="print the result"
	)
	args = parser.parse_args(args)
	APICommand(args.name[0]).create_api(args.print)


@subcmd('config', help='configure igen')
def cmd_project(parser, context, args):
	parser.description='Configure igen.'
	parser.epilog="To configure the project information, run 'igen config project'"
	parser.add_argument(
		'-i', '--info',
		required=False, 
		action='store_true',
		help='show the configuration of the section and exit'
	)
	parser.add_argument(
		'name',
		nargs=1,
		help='section [and its key separated by a dot]'
	)
	parser.add_argument(
		'value',
		nargs='*',
		help='section value'
	)
	args = parser.parse_args(args)
	cmd = ConfigCommand()
	name = args.name[0]
	values = args.value
	if 'project' in args.name:
		if args.info:
			cmd.project_info(True)
		else:
			cmd.update_project_info()
	elif values:
		cmd.config(name, values[0])
	else:
		print('Invalid section and/or key.')


def main():
	handler = ArgumentHandler(
		use_subcommand_help=True,
		epilog='Get help on a subcommand: igen subcommand -h'
	)
	handler.add_argument(
		'-v', '--version', 
		action='version',
		version=__version__,
		help='show the version number and exit'
	)
	handler.run()


if __name__ == '__main__':
	main()

	