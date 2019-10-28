import os.path
import shutil

from distutils.dir_util import copy_tree
from .command import Command


class XCodeCommand(Command):

    def install_templates(self):
        try:
            destination = os.path.join(
                os.path.expanduser("~"),
                r'Library/Developer/Xcode/Templates/File Templates/Custom Templates/'
            )

            copy_tree(
                r'./igen_templates/xcode_templates',
                destination
            )

            print('Install succeeded.')
        except Exception as e:
            print(e)

    def uninstall_templates(self):
        try:
            caFolder = os.path.join(
                os.path.expanduser("~"),
                r'Library/Developer/Xcode/Templates/File Templates/Custom Templates/Clean Architecture.xctemplate/'
            )

            caUTFolder = os.path.join(
                os.path.expanduser("~"),
                r'Library/Developer/Xcode/Templates/File Templates/Custom Templates/Clean Architecture UT.xctemplate/'
            )

            if os.path.isdir(caFolder):
                shutil.rmtree(caFolder)

            if os.path.isdir(caUTFolder):
                shutil.rmtree(caUTFolder)

            print('Uninstall succeeded.')
        except Exception as e:
            print(e)
