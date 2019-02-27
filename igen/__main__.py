from arghandler import subcmd, ArgumentHandler

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


@subcmd('template', help='create template files for a scene')
def cmd_template(parser, context, args):
    parser.epilog = """'list', 'detail', 'form' and 'setting' templates \
require copying the model to the pasteboard before running the command."""
    parser.description = 'Create template files for a scene.'
    parser.add_argument(
        'type',
        nargs=1,
        choices=[
                    'skeleton',
                    'base',
                    'list',
                    'detail',
                    'form',
                    'login',
                    'setting'
                 ],
        help="template type"
    )
    parser.add_argument(
        'name',
        nargs=1,
        help='scene name'
    )
    parser.add_argument(
        '--window',
        required=False,
        action='store_true',
        help='use UIWindow instead of UINavigationController in the Navigator.'
    )
    parser.add_argument(
        '--section',
        required=False,
        action='store_true',
        help="""show the list with header sections ('list' and 'setting' \
templates only)"""
    )
    parser.add_argument(
        '--collection',
        required=False,
        action='store_true',
        help="""use UICollectionView instead of UITableView ('list' \
template only)"""
    )
    parser.add_argument(
        '--static',
        required=False,
        action='store_true',
        help="""display details of the object in a static UITableViewController \
('detail' template only)"""
    )
    parser.add_argument(
        '--submit',
        required=False,
        help="set the name of the submit action ('form' template only)"
    )
    parser.add_argument(
        '--dynamic',
        required=False,
        action='store_true',
        help="""use the dynamic form instead of the static form \
('form' template only)"""
    )
    args = parser.parse_args(args)
    template_name = args.type[0]
    scene_name = args.name[0]
    options = {
        'window': args.window,
        'section': args.section,
        'collection': args.collection,
        'static': args.static,
        'submit': args.submit,
        'dynamic': args.dynamic
    }
    TemplateCommand(template_name, scene_name, options).create_files()


@subcmd('mock', help='create a mock class for a protocol/function')
def cmd_mock(parser, context, args):
    parser.usage = '''copy the protocol/function to the pasteboard then run: \
igen mock [-h] [-p]'''
    parser.description = 'Create a mock class for a protocol/function.'
    parser.add_argument(
        '-p', '--print',
        required=False,
        action='store_true',
        help="print the result"
    )
    args = parser.parse_args(args)
    protocol_text = pasteboard_read()
    MockCommand(protocol_text).create_mock(args.print)


@subcmd('test', help='create unit tests for a view model')
def cmd_test(parser, context, args):
    parser.usage = '''copy the view model to the pasteboard then run: \
igen test [-h] [-p]'''
    parser.description = 'Create unit tests for a view model.'
    parser.add_argument(
        '-p', '--print',
        required=False,
        action='store_true',
        help="print the result"
    )
    args = parser.parse_args(args)
    vm_text = pasteboard_read()
    UnitTestCommand(vm_text).create_tests(args.print)


@subcmd('bind', help='create a bindViewModel method for a UIViewController')
def cmd_bind(parser, context, args):
    parser.usage = '''copy the view model to the pasteboard then run: \
igen bind [-h] [-p]'''
    parser.description = '''Create a bindViewModel method \
for a UIViewController.'''
    parser.add_argument(
        '-p', '--print',
        required=False,
        action='store_true',
        help="print the result"
    )
    args = parser.parse_args(args)
    vm_text = pasteboard_read()
    BindViewModelCommand(vm_text).create_bind_view_model(args.print)


@subcmd('init', help='create a initialize method for a class/struct')
def cmd_init(parser, context, args):
    parser.usage = '''copy the class/struct to the pasteboard then run: \
igen init [-h] [-p]'''
    parser.description = 'Create a initialize method for a class/struct.'
    parser.add_argument(
        '-p', '--print',
        required=False,
        action='store_true',
        help="print the result"
    )
    args = parser.parse_args(args)
    model_text = pasteboard_read()
    InitCommand(model_text).create_init(args.print)


@subcmd('json', help='create a model from JSON')
def cmd_json(parser, context, args):
    parser.usage = '''copy the JSON to the pasteboard then run: \
igen json [-h] [--return-classes] [-p] name'''
    parser.description = 'Create a model from JSON.'
    parser.add_argument(
        'name',
        nargs=1,
        help='model name'
    )
    parser.add_argument(
        '--return-classes',
        required=False,
        action='store_true',
        help="return classes instead of structs"
    )
    parser.add_argument(
        '-p', '--print',
        required=False,
        action='store_true',
        help="print the result"
    )
    args = parser.parse_args(args)
    json = pasteboard_read()
    (JSONCommand(args.name[0], json)
        .create_models(args.print, args.return_classes))


@subcmd('api', help='create input and ouput files for an API')
def cmd_api(parser, context, args):
    parser.description = 'Create input and ouput files for an API.'
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
    parser.description = 'Configure igen.'
    parser.epilog = """To configure the project information, run 'igen config project'. \
To view configuration file, run 'igen config info'."""
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
    if name == 'info':
        cmd.info()
    elif name == 'project':
        cmd.update_project_info()
    elif values:
        cmd.config(args.name[0], values[0])
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
