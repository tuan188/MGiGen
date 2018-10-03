# coding=utf-8

from Constants import FILE_HEADER
from FileHeaderCommand import FileHeaderCommand
from Template import Template
from Pasteboard import pasteboard_read
from datetime import datetime
from Command import Command

class TemplateCommand(Command):
	def __init__(self, template_name, scene_name, options):
		super(TemplateCommand, self).__init__()
		self.template_name = template_name
		self.scene_name = scene_name
		self.options = options

	@classmethod
	def description(cls):
		return "Generate template files"

	@classmethod
	def name(cls):
		return "template"

	def create_files(self):
		try:
			with open(FILE_HEADER) as f:
				content = f.readlines()
				info = [x.strip() for x in content]
				project = info[0]
				developer = info[1]
				company = info[2]
		except:
			project, developer, company = FileHeaderCommand().update_file_header()
		now = datetime.now()
		date = "{}/{}/{}".format(now.month, now.day, now.strftime("%y"))
		if self.template_name == Template.TemplateType.BASE:
			template = Template.BaseTemplate(self.scene_name, project, developer, company, date)
			template.create_files()
			print("Finish!")
		elif self.template_name == Template.TemplateType.LIST:
			model_text = pasteboard_read()
			try:
				model = Template().parse_model(model_text)
				template = Template.ListTemplate(model, self.options, self.scene_name, project, developer, company, date)
				template.create_files()
				print("Finish!")
			except:
				print('Invalid model text in clipboard.')
		elif self.template_name == Template.TemplateType.DETAIL:
			model_text = pasteboard_read()
			try:
				model = Template().parse_model(model_text)
				if "--static" in self.options:
					template = Template.StaticDetailTemplate(model, self.options, self.scene_name, project, developer, company, date)
				else:
					template = Template.DetailTemplate(model, self.options, self.scene_name, project, developer, company, date)
				template.create_files()
				print("Finish!")
			except:
				print('Invalid model text in clipboard.')
		else:
			print("Invalid template name.")

