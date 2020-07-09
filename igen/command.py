# coding=utf-8


class Command:

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
        return (format("   " + cls.name(), Command.TAB_LENGTH)
                + cls.description())

    @classmethod
    def help(cls):
        return cls.long_description()


class CommandOption:

    def __init__(self, options):
        self._options = options

    def __getattr__(self, name):
        cls = type(self)
        if name in self._options:
            return self._options[name]
        else:
            msg = '{.__name__!r} object has no attribute {!r}'
            raise AttributeError(msg.format(cls, name))
