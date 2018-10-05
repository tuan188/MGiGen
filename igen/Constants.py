# coding=utf-8

FILE_HEADER = "project_info.txt"

SWIFT_TYPES_DEFAULT_VALUES = {
	"Int": "0",
	"Bool": "false",
	"String": '""',
	"Double": "0.0",
	"Float": "0.0",
	"Date": "Date()"
}

SWIFT_TYPES = { 
	"Int", 
	"Bool", 
	"String", 
	"Double", 
	"Float"
	"Date"
}

class Commands:
	HELP = "help"
	HEADER = "header"
	TEMPLATE = "template"
	JSON = "json"
	MOCK = "mock"
	API = "api"
	UNIT_TEST = "test"
	BIND_VIEW_MODEL = "bind"
	INIT = "init"