# coding=utf-8

import sys
from .constants import FILE_HEADER
from .command import Command

class FileHeaderCommand(Command):
	def __init__(self):
		super(FileHeaderCommand, self).__init__()

	@classmethod
	def description(cls):
		return "Update file header info"

	@classmethod
	def name(cls):
		return "header"

	def update_file_header(self):
		project = input('Enter project name: ')
		developer = input('Enter developer name: ')
		company = input('Enter company name: ')
		content = "\n".join([project, developer, company])
		with open(FILE_HEADER, "w") as f:	
			f.write(content)
		return (project, developer, company)