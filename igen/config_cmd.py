# coding=utf-8

import os.path
import os
import configparser
from .command import Command


class ConfigCommand(Command):

    KEY_VALUES = {
        'project.name': 'str',
        'project.developer': 'str',
        'project.company': 'str',
        'output.path': 'str'
    }

    @property
    def config_file(self):
        return os.path.join(os.path.expanduser("~"), '.igen')

    def update_project_info(self):
        project = input('Enter project name: ')
        developer = input('Enter developer name: ')
        company = input('Enter company name: ')
        config = configparser.ConfigParser()
        config.read(self.config_file)
        if 'project' not in config:
            config['project'] = {}
        config['project']['name'] = project
        config['project']['developer'] = developer
        config['project']['company'] = company
        # write to file
        with open(self.config_file, "w") as f:
            config.write(f)
        return (project, developer, company)

    def project_info(self, print_result):
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file)
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
            with open(self.config_file, "r") as f:
                content = f.readlines()
                print(''.join(content))
        except Exception as e:
            print(e)

    def output_path(self):
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file)
            return config['output']['path']
        except Exception:
            return None

    def config(self, name, value):
        if name not in ConfigCommand.KEY_VALUES:
            print('Invalid section and/or key.')
            return
        try:
            config = configparser.ConfigParser()
            config.read(self.config_file)
            (section, section_item) = name.split('.')
            if section not in config:
                config[section] = {}
            if value == '@here':
                value = os.getcwd()
            config[section][section_item] = value
            with open(self.config_file, "w") as f:
                config.write(f)
            self.info()
        except Exception as e:
            print(e)
