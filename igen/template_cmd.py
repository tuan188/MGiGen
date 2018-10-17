# coding=utf-8

from subprocess import call
from .config_cmd import ConfigCommand
from .template import Template, ProjectInfo
from .pb import pasteboard_read
from .command import Command

class TemplateCommand(Command):
	def __init__(self, template_name, scene_name, options):
		super(TemplateCommand, self).__init__()
		self.template_name = template_name
		self.scene_name = scene_name
		self.options = options

	def create_files(self):
		info = ConfigCommand().project_info(False)
		if info != None:
			project, developer, company = info
		else:
			project, developer, company = ConfigCommand().update_project_info()
		project_info = ProjectInfo(project, developer, company)
		if self.template_name == Template.TemplateType.BASE:
			template = Template.BaseTemplate(self.scene_name, project_info)
			template.create_files()
		elif self.template_name == Template.TemplateType.LIST:
			model_text = pasteboard_read()
			try:
				model = Template().parse_model(model_text)
			except:
				print("The model in the pasteboard is invalid.")
				exit(1)
			template = Template.ListTemplate(model, self.options, self.scene_name, project_info)
			template.create_files()
		elif self.template_name == Template.TemplateType.DETAIL:
			model_text = pasteboard_read()
			try:
				model = Template().parse_model(model_text)
			except:
				print("The model in the pasteboard is invalid.")
				exit(1)
			if self.options['static']:
				template = Template.StaticDetailTemplate(model, self.options, self.scene_name, project_info)
			else:
				template = Template.DetailTemplate(model, self.options, self.scene_name, project_info)
			template.create_files()
		else:
			print("Invalid template type.")
			exit(1)
		targetDirectory = "./{}".format(self.scene_name)
		call(["open", targetDirectory])

