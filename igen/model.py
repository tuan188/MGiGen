# coding=utf-8

import re
from jinja2 import Environment, PackageLoader
from .constants import (SWIFT_TYPES_DEFAULT_VALUES,
                        SWIFT_TYPES_MOCK_VALUES,
                        SWIFT_TYPES)
from .str_helpers import upper_first_letter, lower_first_letter, is_number


class Model(object):

    PROPERTY_PATTERN = r'(?:let|var) (\w+)(?:: ([^=\s]*))?(?: = ([^/\n]+))?(?:\s*//.*)?'
    MODEL_PATTERN = r'(?:struct|class|extension) (\w+)(?::\s)*(?:\w+,?\s?)* {([^}]+)'
    ENUM_PATTERN = r'(\w+)\.(\w+)'
    DIC_PATTERN = r'^\[\w*:\s?.*\]$'

    class Property(object):
        def __init__(self, property):
            self.property = property
            property_regex = re.compile(Model.PROPERTY_PATTERN)
            mo = property_regex.search(property)
            self.name = mo.group(1)
            self.name_title = upper_first_letter(self.name)
            self.type = Model.PropertyType(mo.group(2), mo.group(3))

        @property
        def is_url(self):
            lowered_name = self.name.lower()

            if lowered_name.endswith("id"):
                return False

            return "image" in lowered_name or "url" in lowered_name

    class PropertyType(object):
        def __init__(self, name, value):
            self.custom_types = {}

            if name is None:
                if value.startswith('"'):
                    self.name = 'String'
                elif value.endswith('()'):
                    self.name = value[:-2]
                elif value == 'true' or value == 'false':
                    self.name = 'Bool'
                elif is_number(value):
                    if '.' in value:
                        self.name = 'Double'
                    else:
                        self.name = 'Int'
                else:
                    mo = re.search(Model.ENUM_PATTERN, value)
                    if mo:
                        self.name = mo.group(1)
                        self.custom_types[self.name] = value
                    else:
                        self.name = 'Any'
            else:
                self.name = name

        @property
        def is_optional(self):
            return self.name.startswith('Optional<') or self.name.endswith("?")

        @property
        def is_array(self):
            return self.name.startswith('Array<') or (self.name.endswith("]") and ':' not in self.name)

        @property
        def is_dictionary(self):
            return self.name.startswith('Dictionary<') or (self.name.endswith("]") and ':' in self.name)

        @property
        def is_observable(self):
            return self.name.startswith('Observable<')

        @property
        def is_driver(self):
            return self.name.startswith('Driver<')

        @property
        def default_value(self):
            if self.is_optional:
                value = "nil"
            elif self.is_array:
                value = "[]"
            elif self.is_dictionary:
                value = "[:]"
            elif self.name in SWIFT_TYPES:
                value = SWIFT_TYPES_DEFAULT_VALUES[self.name]
            elif self.name in self.custom_types:
                value = self.custom_types[self.name]
            elif self.is_observable:
                value = 'Observable.empty()'
            elif self.is_driver:
                value = 'Driver.empty()'
            else:
                value = "{}()".format(self.name)
            return value

        @property
        def mock_value(self):
            if self.name in SWIFT_TYPES:
                return SWIFT_TYPES_MOCK_VALUES[self.name]
            else:
                return self.default_value

    def __init__(self, name, properties):
        self.name = name
        self.properties = properties

    @classmethod
    def from_string(cls, string):
        model_regex = re.compile(Model.MODEL_PATTERN)
        match = model_regex.search(string)
        model_name = match.group(1)
        property_block = match.group(2)
        property_regex = re.compile(Model.PROPERTY_PATTERN)

        properties = [Model.Property(m.group())
                      for m in property_regex.finditer(property_block)]

        return cls(model_name, properties)


class InitModel(Model):

    def create_init(self):
        env = Environment(
            loader=PackageLoader('igen_templates', 'commands'),
            trim_blocks=True,
            lstrip_blocks=True
        )

        template = env.get_template('Init.swift')

        content = template.render(
            name=self.name,
            properties=self.properties
        )

        return content


class Enum(object):
    def __init__(self, name, cases):
        self.name = name
        self.name_variable = lower_first_letter(name)
        self.cases = cases
        self.cases_title = [upper_first_letter(c) for c in cases]
        self.case_count = len(cases)

    @classmethod
    def from_string(cls, enum_string):
        enum_regex = re.compile(r'enum (\w+)[^{]* {([\d\D]*)}')
        match = enum_regex.search(enum_string)
        enum_name = match.group(1)
        enum_block = match.group(2)
        regex = re.compile(r'case (\w+)')
        cases = [m.group(1) for m in regex.finditer(enum_block)]
        return cls(enum_name, cases)
