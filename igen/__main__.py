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
from .encoder import Encoder
from .file_header_cmd import FileHeaderCommand


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
    model_string = pasteboard_read()
    InitCommand(model_string).create_init(args.print)


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


@subcmd('config', help='configure the tool')
def cmd_config(parser, context, args):
    parser.description = 'Configure the tool.'
    parser.epilog = """To configure the project information, run 'igen config project'. \
To view the configuration file, run 'igen config info'. \
To delete the configuration file, run 'igen config delete. \
To view the available configurations, run 'igen config keys'."""

    parser.add_argument(
        'key',
        nargs='?',
        help='configuration key'
    )
    parser.add_argument(
        'value',
        nargs='?',
        help='configuration value'
    )
    parser.add_argument(
        '--global',
        required=False,
        action='store_true',
        help="global configuration"
    )
    parser.add_argument(
        '--unset',
        required=False,
        action='store_true',
        help="remove a setting"
    )
    args = parser.parse_args(args)
    global_config = vars(args)['global']

    cmd = ConfigCommand(global_config)
    key = args.key
    value = args.value
    unset = args.unset

    if key is None:
        cmd.info()
    elif key == 'project':
        cmd.update_project_info()
    elif key == 'delete':
        cmd.delete_config()
    elif key == 'keys':
        cmd.keys()
    elif unset:
        cmd.unset(key)
    elif value:
        cmd.config(key, value)
    else:
        print('Invalid configuration key.')


@subcmd('encode', help='encode a string')
def cmd_encode(parser, context, args):
    parser.epilog = 'encode a string.'
    parser.description = 'Encode a string.'
    parser.add_argument(
        'algorithm',
        nargs=1,
        choices=[
            'md5'
        ],
        help='algorithm'
    )
    parser.add_argument(
        'string',
        nargs=1,
        help='the input string'
    )
    args = parser.parse_args(args)
    alg = args.algorithm[0]
    string = args.string[0]
    encoder = Encoder()
    print(encoder.encode(alg, string))


@subcmd('header', help="update files' headers")
def cmd_file_header(parser, context, args):
    parser.epilog = "update files' headers."
    parser.description = "Update files' headers."
    parser.add_argument(
        'paths',
        nargs='+',
        help="files' paths"
    )
    parser.add_argument(
        '--file-name',
        required=False,
        action='store_true',
        help='update file name'
    )
    parser.add_argument(
        '--project',
        required=False,
        action='store_true',
        help='update project'
    )
    parser.add_argument(
        '--developer',
        required=False,
        action='store_true',
        help='update developer'
    )
    parser.add_argument(
        '--created-date',
        required=False,
        action='store_true',
        help='update created date'
    )
    parser.add_argument(
        '--copyright-year',
        required=False,
        action='store_true',
        help='update copyright year'
    )
    parser.add_argument(
        '--company',
        required=False,
        action='store_true',
        help='update company'
    )
    args = parser.parse_args(args)

    options = {
        'update_file_name': args.file_name,
        'update_project': args.project,
        'update_developer': args.developer,
        'update_created_date': args.created_date,
        'update_copyright_year': args.copyright_year,
        'update_company': args.company,
    }

    paths = args.paths
    cmd = FileHeaderCommand(paths, options)
    cmd.update_header()


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
