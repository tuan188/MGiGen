# coding=utf-8

from subprocess import call

from .config_cmd import ConfigCommand
from .template import Template, ProjectInfo
from .pb import pasteboard_read
from .command import Command, CommandOption
from .encoder import Encoder
from .model import Model, Enum


class TemplateCommand(Command):
    def __init__(self, template_name, scene_name, options):
        super(TemplateCommand, self).__init__()
        self.template_name = template_name
        self.scene_name = scene_name
        self.options = CommandOption(options)

    def create_files(self):
        config_command = ConfigCommand(global_config=None)
        info = config_command.project_info(print_result=False)
        if info is not None:
            project, developer, company = info
        else:
            project, developer, company = config_command.update_project_info()

        project_id = config_command.project_id()
        if project_id == '@project':
            encoder = Encoder()
            project_id = encoder.encode('md5', project)

        project_info = ProjectInfo(project, developer, company, project_id)
        if self.template_name == Template.TemplateType.BASE:
            template = Template.BaseTemplate(
                self.options,
                self.scene_name,
                project_info
            )
            output_path = template.create_files()
        elif self.template_name == Template.TemplateType.LIST:
            model_string = pasteboard_read()
            try:
                model = Model.from_string(model_string)
            except Exception:
                print("The model in the pasteboard is invalid.")
                exit(1)
            template = Template.ListTemplate(
                model,
                self.options,
                self.scene_name,
                project_info
            )
            output_path = template.create_files()
        elif self.template_name == Template.TemplateType.DETAIL:
            model_string = pasteboard_read()
            try:
                model = Model.from_string(model_string)
            except Exception:
                print("The model in the pasteboard is invalid.")
                exit(1)
            if self.options.static:
                template = Template.StaticDetailTemplate(
                    model,
                    self.options,
                    self.scene_name,
                    project_info
                )
            else:
                template = Template.DetailTemplate(
                    model,
                    self.options,
                    self.scene_name,
                    project_info
                )
            output_path = template.create_files()
        elif self.template_name == Template.TemplateType.SKELETON:
            template = Template.SkeletonTemplate(
                self.options,
                self.scene_name,
                project_info
            )
            output_path = template.create_files()
        elif self.template_name == Template.TemplateType.FORM:
            model_string = pasteboard_read()
            try:
                model = Model.from_string(model_string)
            except Exception:
                print("The model in the pasteboard is invalid.")
                exit(1)
            if self.options.dynamic:
                template = Template.DynamicFormTemplate(
                    model,
                    self.options,
                    self.scene_name,
                    project_info
                )
            else:
                template = Template.FormTemplate(
                    model,
                    self.options,
                    self.scene_name,
                    project_info
                )
            output_path = template.create_files()
        elif self.template_name == Template.TemplateType.LOGIN:
            template = Template.LoginTemplate(
                self.options,
                self.scene_name,
                project_info
            )
            output_path = template.create_files()
        elif self.template_name == Template.TemplateType.SETTING:
            enum_string = pasteboard_read()
            try:
                enum = Enum.from_string(enum_string)
            except Exception:
                print("The enum in the pasteboard is invalid.")
                exit(1)
            template = Template.SettingTemplate(
                enum,
                self.options,
                self.scene_name,
                project_info
            )
            output_path = template.create_files()
        else:
            print("Invalid template type.")
            exit(1)
        if output_path is not None:
            try:
                call(["open", output_path])
            except Exception as e:
                print(e)
                pass
