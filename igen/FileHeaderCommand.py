# coding=utf-8

from Constants import FILE_HEADER

class FileHeaderCommand(object):
	def __init__(self):
		super(FileHeaderCommand, self).__init__()

	def update_file_header(self):
		project = raw_input('Enter project name: ')
		developer = raw_input('Enter developer name: ')
		company = raw_input('Enter company name: ')
		content = "\n".join([project, developer, company])
		with open(FILE_HEADER, "w") as f:	
			f.write(content)
		return (project, developer, company)