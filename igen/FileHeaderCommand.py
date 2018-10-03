# coding=utf-8

from Constants import FILE_HEADER
from Command import Command

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
		project = raw_input('Enter project name: ')
		developer = raw_input('Enter developer name: ')
		company = raw_input('Enter company name: ')
		content = "\n".join([project, developer, company])
		with open(FILE_HEADER, "w") as f:	
			f.write(content)
		return (project, developer, company)