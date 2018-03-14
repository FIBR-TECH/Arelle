'''
pluginPackages test case

(c) Copyright 2012 Mark V Systems Limited, All rights reserved.
'''

def foo():
	print ("imported packaged plug-in child 2")

__pluginInfo__ = {
    'name': 'Package Listed Import Child 2',
    'version': '0.9',
    'description': "This is a packaged child plugin.",
    'license': 'Apache-2',
    'author': 'Mark V Systems',
    'copyright': '(c) Copyright 2015 Mark V Systems Limited, All rights reserved.',
    # classes of mount points (required)
    'Import.Packaged.Entry3': foo,
    # import plugins
    'import': ('importTestGrandchild1.py', 'importTestGrandchild2.py')
}
