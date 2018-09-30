from setuptools import setup
setup(
	name = 'igen',
	version = '1.0.0',
	packages = ['igen', 'igen_templates'],
	entry_points = {
		'console_scripts': [
			'igen = igen.__main__:main'
		]
	},
	include_package_data = True
	)