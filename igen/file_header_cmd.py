import re
from datetime import datetime
import os

from jinja2 import Environment, PackageLoader

from .command import Command, CommandOption
from .config_cmd import ConfigCommand
from .template import ProjectInfo
from .encoder import Encoder


class FileHeaderCommand(Command):

    def __init__(self, file_paths, options):
        self.file_paths = file_paths
        self.options = CommandOption(options)
        self.env = Environment(
            loader=PackageLoader('igen_templates', 'commands'),
            trim_blocks=True,
            lstrip_blocks=True
        )

    def update_header(self):
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

        for file_path in self.file_paths:
            self._update_header(file_path, project_info)

    def _update_header(self, file_path, project_info):
        with open(file_path, 'rt', encoding='utf-8') as f:
            data = f.readlines()
        file_content = ''.join(data)

        header_regex_string = r"""//
// +(.+)
// +(.+)
//
// +Created by (.+?) on (\d+/\d+/\d+).
// +Copyright © (\d{4}) (.+?). All rights reserved.
//"""

        header_regex = re.compile(header_regex_string)
        matches = header_regex.findall(file_content)

        if matches and any([
                self.options.update_file_name,
                self.options.update_project,
                self.options.update_developer,
                self.options.update_created_date,
                self.options.update_copyright_year,
                self.options.update_company
        ]):
            file_name, project, developer, date_string, \
                copyright_year, company = matches[0]
            update_all = False
        else:
            update_all = True

        if update_all or self.options.update_file_name:
            file_name = os.path.basename(file_path)
        if update_all or self.options.update_project:
            if project_info.project_id:
                project = '{} ({})'.format(
                    project_info.project,
                    project_info.project_id
                )
            else:
                project = project_info.project
        if update_all or self.options.update_developer:
            developer = project_info.developer
        if update_all or self.options.update_created_date:
            now = datetime.now()
            date_string = "{}/{}/{}".format(
                now.month,
                now.day,
                now.strftime("%y")
            )
        if update_all or self.options.update_copyright_year:
            copyright_year = datetime.now().year
        if update_all or self.options.update_company:
            company = project_info.company

        template = self.env.get_template("FileHeader.swift")
        header = template.render(
            file_name=file_name,
            project=project,
            developer=developer,
            created_date=date_string,
            copyright_year=copyright_year,
            company=company
        )

        if matches:
            file_content = header_regex.sub(
                header,
                file_content
            )
        else:
            file_content = header + '\n\n' + file_content

        with open(file_path, 'wt', encoding='utf-8') as f:
            f.write(file_content)
            print('Updated:', file_path)
