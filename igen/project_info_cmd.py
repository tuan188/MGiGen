# coding=utf-8

import sys
from .constants import FILE_HEADER
from .command import Command

class ProjectInfoCommand(Command):

	@classmethod
	def description(cls):
		return "Update file header info"

	@classmethod
	def name(cls):
		return "header"

	def update_info(self):
		project = input('Enter project name: ')
		developer = input('Enter developer name: ')
		company = input('Enter company name: ')
		content = "\n".join([project, developer, company])
		with open(FILE_HEADER, "w") as f:	
			f.write(content)
		return (project, developer, company)

	def info(self):
		try:
			with open(FILE_HEADER) as f:
				content = f.readlines()
				info = [x.strip() for x in content]
				project = info[0]
				developer = info[1]
				company = info[2]
			print('Project: {}\nDeveloper: {}\nCompany: {}'.format(project, developer, company))
		except:
			pass