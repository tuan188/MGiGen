import sys
from .igen import execute

def main():
	print('in main')
	args = sys.argv[1:]
	execute(args)

if __name__ == '__main__':
	main()