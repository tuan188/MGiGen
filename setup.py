from setuptools import setup
from igen import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name = 'igen',
	version = __version__,
	author="Tuan Truong",
	author_email="tuan188@gmail.com",
	description="Code Generation Tools for iOS",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/tuan188/MGiOSTools",
	license='MIT',
	packages = ['igen', 'igen_templates'],
	entry_points = {
		'console_scripts': [
			'igen = igen.__main__:main'
		]
	},
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	python_requires=">=3",
	install_requires=['Jinja2>=2.10', 'arghandler>=1.2'],
	include_package_data = True
	)