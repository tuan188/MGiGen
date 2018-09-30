from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name = 'igen',
	version = '1.0.4',
	author="Tuan Truong",
	author_email="tuan188@gmail.com",
	description="Code Generator Tools for iOS",
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
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
	python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
	install_requires=['Jinja2>=2.10'],
	include_package_data = True
	)