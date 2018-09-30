import sys
from .igen import execute
from .igen import HelpCommand

def main():
	if len(sys.argv) > 1:
		args = sys.argv[1:]
		execute(args)
	else:
		HelpCommand().show_help()

if __name__ == '__main__':
	main()