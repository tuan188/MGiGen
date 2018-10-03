# coding=utf-8

class HelpCommand(object):
	def __init__(self):
		super(HelpCommand, self).__init__()
		
	def show_help(self):
		help = "igen commands:\n\n"
		help += format("   help", "<15") + "Show help\n"
		help += format("   header", "<15") + "Update file header info\n"
		help += format("   template", "<15") + "Generate template files\n"
		help += format("   json", "<15") + "Create models from json text\n"
		help += format("   mock", "<15") + "Create mock from protocol\n"
		help += format("   api", "<15") + "Create API request\n"
		help += format("   test", "<15") + "Create Unit Tests from view model\n"
		help += format("   bind", "<15") + "Create bindViewModel method for view controller from view model\n"
		help += format("   init", "<15") + "Create init method for struct model\n"
		# help += "\n"
		# help += "Get help on a command: igen help [command]\n"
		print(help)