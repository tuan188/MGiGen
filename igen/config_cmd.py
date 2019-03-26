# coding=utf-8

import os.path
import os
import configparser
import itertools

from .command import Command


class ConfigCommand(Command):

    GLOBAL_CONFIG_FILE = '.igen'
    LOCAL_CONFIG_FILE = 'igen.config'

    KEY_VALUES = {
        'project.name': 'str',
        'project.developer': 'str',
        'project.company': 'str',
        'project.id': 'str',
        'output.path': 'str'
    }

    def __init__(self, global_config):
        self.global_config = global_config

    @property
    def default_global_config_file_path(self):
        return os.path.join(os.path.expanduser("~"), self.GLOBAL_CONFIG_FILE)

    @property
    def global_config_exists(self):
        return os.path.isfile(self.default_global_config_file_path)

    @property
    def default_local_config_file_path(self):
        return './{}'.format(self.LOCAL_CONFIG_FILE)

    @property
    def local_config_exists(self):
        return os.path.isfile(self.default_local_config_file_path)

    def get_local_config_file_path(self):
        current_folder = os.getcwd()
        folders = current_folder.split('/')

        # remove empty path
        folders = [f for f in folders if f != '']
        paths = list(itertools.accumulate(
            folders,
            lambda x, y: '{}/{}'.format(x, y))
        )
        paths = ['/'] + ['/{}/'.format(p) for p in paths]

        file_paths = [p + self.LOCAL_CONFIG_FILE for p in reversed(paths)]

        for file_path in file_paths:
            if os.path.isfile(file_path):
                return file_path
        return None

    @property
    def config_file_path(self):
        if self.global_config is None:  # for template command
            file_path = self.get_local_config_file_path()
            if file_path is not None:
                return file_path
            elif self.global_config_exists:
                return self.default_global_config_file_path
            else:
                return self.default_local_config_file_path
        elif self.global_config:  # for config command
            return self.default_global_config_file_path
        else:
            file_path = self.get_local_config_file_path()
            if file_path is not None:
                return file_path
            return self.default_local_config_file_path

    def update_project_info(self):
        project = input('Enter project name: ')
        developer = input('Enter developer name: ')
        company = input('Enter company name: ')

        config = configparser.ConfigParser()
        config.read(self.config_file_path)

        if 'project' not in config:
            config['project'] = {}

        config['project']['name'] = project
        config['project']['developer'] = developer
        config['project']['company'] = company

        # write to file
        with open(self.config_file_path, "w") as f:
            config.write(f)
        return (project, developer, company)

    def project_info(self, print_result):
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file_path)
            project = config['project']['name']
            developer = config['project']['developer']
            company = config['project']['company']

            if print_result:
                print('Project: {}\nDeveloper: {}\nCompany: {}'
                      .format(project, developer, company))

            return (project, developer, company)
        except Exception:
            return None

    def info(self):
        try:
            with open(self.config_file_path, "r") as f:
                content = f.readlines()
                if self.global_config:
                    print('Global configuration:\n')
                else:
                    print('Local configuration:\n')
                print(''.join(content))
        except Exception:
            print("The configuration file does not exist.")

    def output_path(self):
        return self.read_config('output.path')

    def project_id(self):
        return self.read_config('project.id')

    def read_config(self, name):
        if name not in ConfigCommand.KEY_VALUES:
            return None
        try:
            (section, section_item) = name.split('.')
            config = configparser.ConfigParser()
            config.read(self.config_file_path)
            return config[section][section_item]
        except Exception:
            return None

    def config(self, name, value):
        if name not in ConfigCommand.KEY_VALUES:
            print('Invalid section and/or key.')
            return
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file_path)

            (section, section_item) = name.split('.')

            if section not in config:
                config[section] = {}

            if value == '@here':
                value = os.getcwd()
            elif value == '@desktop':
                value = os.path.join(os.path.expanduser("~"), 'Desktop/')
            elif value == '@downloads':
                value = os.path.join(os.path.expanduser("~"), 'Downloads/')
            elif value == '@documents':
                value = os.path.join(os.path.expanduser("~"), 'Documents/')

            config[section][section_item] = value

            with open(self.config_file_path, 'w') as f:
                config.write(f)

            self.info()
        except Exception as e:
            print(e)

    def delete_config(self):
        if os.path.exists(self.config_file_path):
            os.remove(self.config_file_path)
            print('Successfully removed the configuration file.')
        else:
            print('The configuration file does not exist.')

    def keys(self):
        print('Available configuration keys:')
        for key in self.KEY_VALUES.keys():
            print('   ', key)

    def unset(self, name):
        if name not in ConfigCommand.KEY_VALUES:
            print('Invalid section and/or key.')
            return

        if not os.path.exists(self.config_file_path):
            print('The configuration file does not exist.')
            return

        try:
            config = configparser.ConfigParser()
            config.read(self.config_file_path)

            (section, section_item) = name.split('.')

            if section in config and section_item in config[section]:
                del config[section][section_item]

            with open(self.config_file_path, 'w') as f:
                config.write(f)

            self.info()
        except Exception as e:
            print(e)
