# coding=utf-8

class Command(object):

	TAB_LENGTH = "<15"

	@classmethod
	def description(cls):
		return ""

	@classmethod
	def name(cls):
		return ""

	@classmethod
	def class_name(cls):
		return cls.__name__

	@classmethod
	def long_description(cls):
		return format("   " + cls.name(), Command.TAB_LENGTH) + cls.description()

	@classmethod
	def help(cls):
		return cls.long_description()
