import sys
import argparse
from arghandler import *

from . import __version__
from .pb import pasteboard_read
from .api_cmd import APICommand
from .mock_cmd import MockCommand
from .init_cmd import InitCommand
from .project_info_cmd import ProjectInfoCommand
from .json_cmd import JSONCommand
from .test_cmd import UnitTestCommand
from .bind_cmd import BindViewModelCommand
from .template_cmd import TemplateCommand

@subcmd('template', help='create template files for the scene')
def cmd_template(parser, context, args):
	parser.epilog="'list' and 'detail' template require copying the Model to the pasteboard before running the command."
	parser.add_argument(
		'-t', '--type',
		required=False, 
		choices=['base', 'list', 'detail'],
		default='base',
		help='template type'
	)
	parser.add_argument(
		'-n', '--name',  
		required=True, 
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
	template_name = args.type
	scene_name = args.name
	options = {
		'section': args.section,
		'collection': args.collection,
		'static': args.static,
	}
	TemplateCommand(template_name, scene_name, options).create_files()


@subcmd('project', help='update the project information')
def cmd_project(parser, context, args):
	parser.add_argument(
		'-i', '--info',
		required=False, 
		action='store_true',
		help='show the project information and exit'
	)
	args = parser.parse_args(args)
	cmd = ProjectInfoCommand()
	if args.info:
		cmd.info()
	else:
		cmd.update_info()


@subcmd('mock', help='create mock for the protocol')
def cmd_mock(parser, context, args):
	parser.usage = 'copy the protocol to the pasteboard then run: igen mock [-h] [-p]'
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
	parser.usage = 'copy the JSON to the pasteboard then run: igen json [-h] -n NAME [-p]'
	parser.add_argument(
		'-n', '--name',
		required=True, 
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
	JSONCommand(args.name, json).create_models(args.print)


@subcmd('api', help='create input and ouput files for the API')
def cmd_api(parser, context, args):
	parser.add_argument(
		'-n', '--name',
		required=True, 
		help='api name'
	)
	parser.add_argument(
		'-p', '--print', 
		required=False, 
		action='store_true', 
		help="print the result"
	)
	args = parser.parse_args(args)
	APICommand(args.name).create_api(args.print)


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

	