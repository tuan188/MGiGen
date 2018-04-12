# coding=utf-8
# Created by Tuan Truong on 2018-04-12.
# © 2018 Framgia.
# v1.0.0

import sys
import os
import subprocess

def to_camel(word):
	return word[0].lower() + word[1:]

def pasteboard_write(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

def create_api(name):
	content = "// MARK: - {}\n".format(name)
	content += "extension API {\n"
	content += "    func {}(_ input: {}Input) -> Observable<{}Output> {{\n".format(to_camel(name), name, name)
	content += "        return request(input)\n"
	content += "    }\n\n"
	content += "    final class {}Input: InputBase {{\n".format(name)
	content += "        init() {\n"
	content += "            super.init(urlString: API.Urls.{},\n".format(to_camel(name))
	content += "                       parameters: nil,\n"
	content += "                       requestType: .get,\n"
	content += "                       requireAccessToken: true)\n"
	content += "        }\n    }\n\n"
	content += "    final class {}Output: OutputBase {{\n".format(name)
	content += "        override func mapping(map: Map) {\n"
	content += "            super.mapping(map: map)\n"
	content += "        }\n    }\n}\n"

	return content

if len(sys.argv) > 1:
	name = sys.argv[1]
else:
	name = raw_input('Enter API name: ')
output = create_api(name)
pasteboard_write(output)
print("Text has been copied to clipboard.")

