# coding=utf-8

import sys
import os.path
import configparser
from .command import Command

class ConfigCommand(Command):

	KEY_VALUES = {
		'project.name': 'str',
		'project.developer': 'str',
		'project.company': 'str'
	}

	@property
	def config_file(self):
		return os.path.join(os.path.expanduser("~"), '.igen')

	def update_project_info(self):
		project = input('Enter project name: ')
		developer = input('Enter developer name: ')
		company = input('Enter company name: ')
		content = "\n".join([project, developer, company])
		config = configparser.ConfigParser()
		config['project'] = {
			'name': project,
			'developer': developer,
			'company': company
		}
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
				print('Project: {}\nDeveloper: {}\nCompany: {}'.format(project, developer, company))
			return (project, developer, company)
		except:
			return None

	def config(self, name, value):
		if not name in ConfigCommand.KEY_VALUES:
			print('Invalid section and/or key.')
			return
		try:
			config = configparser.ConfigParser()
			config.read(self.config_file)
			(section, section_item) = name.split('.')
			config[section][section_item] = value 
			with open(self.config_file, "w") as f:	
				config.write(f)
		except Exception as e:
			print(e)
