from it import pasteboard_read, API, Mock, BindViewModel, UnitTest, Commands, JSON, InitModel
from workflow import Workflow, ICON_ERROR
import sys

def main(wf):
	if len(wf.args):
		command = wf.args[0]
		if command == Commands.API:
			api_name = wf.args[1]
			output = API(api_name).create_api()
			wf.add_item(title = "API",
						subtitle = "Copy result to clipboard",
						arg = output,
						valid = True)
			wf.send_feedback()
		elif command == Commands.MOCK:
			try: 
				protocol_text = pasteboard_read()
				output = Mock(protocol_text).create_mock()
				wf.add_item(title = "Mock",
							subtitle = "Copy result to clipboard",
							arg = output,
							valid = True)
			except:
				wf.add_item(title = "Mock",
							subtitle = "Invalid view model text in clipboard",
							valid = False, 
							icon = ICON_ERROR)
			wf.send_feedback()
		elif command == Commands.BIND_VIEW_MODEL:
			try: 
				vm_text = pasteboard_read()
				output = BindViewModel(vm_text).create_bind_view_model()
				wf.add_item(title = "bindViewModel",
							subtitle = "Copy result to clipboard",
							arg = output,
							valid = True)
			except:
				wf.add_item(title = "bindViewModel",
							subtitle = "Invalid view model text in clipboard",
							valid = False, 
							icon = ICON_ERROR)
			wf.send_feedback()
		elif command == Commands.UNIT_TEST:
			try: 
				vm_text = pasteboard_read()
				output = UnitTest(vm_text).create_tests()
				wf.add_item(title = "Unit Tests",
							subtitle = "Copy result to clipboard",
							arg = output,
							valid = True)
			except:
				wf.add_item(title = "Unit Tests",
							subtitle = "Invalid view model text in clipboard",
							valid = False, 
							icon = ICON_ERROR)
			wf.send_feedback()
		elif command == Commands.JSON:
			model_name = wf.args[1]
			try: 
				json_text = pasteboard_read()
				output = JSON(model_name, json_text).create_models()
				wf.add_item(title = "JSON Parser",
							subtitle = "Copy result to clipboard",
							arg = output,
							valid = True)
			except:
				wf.add_item(title = "InputBuilder",
							subtitle = "Invalid json text in clipboard",
							valid = False, 
							icon = ICON_ERROR)
			wf.send_feedback()
		elif command == Commands.INIT:
			try: 
				model_text = pasteboard_read()
				output = InitModel(model_text).create_init()
				wf.add_item(title = "Init",
							subtitle = "Copy result to clipboard",
							arg = output,
							valid = True)
			except:
				wf.add_item(title = "Init",
							subtitle = "Invalid model text in clipboard",
							valid = False, 
							icon = ICON_ERROR)
			wf.send_feedback()

if __name__ == u"__main__":
	wf = Workflow()
	sys.exit(wf.run(main))

