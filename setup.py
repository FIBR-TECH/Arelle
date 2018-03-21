from distutils.core import setup
setup(
  name = 'arelle',
  packages = ['arelle'], # this must be the same as the name above
  package_data={'arelle': ['config/*', 'plugin/*', 'pyparsing/*', '__pycache__/*']},
  version = '1.0.6',
  description = 'arelle xblr modified by Lendflo',
  author = 'Remi Tuyaerts / Przemyslaw Winszczyk',
  author_email = 'remi.tuyaerts@lendflo.com',
  url = 'https://github.com/LendFlo/pip-arelle', # use the URL to the github repo
  download_url = 'https://github.com/LendFlo/pip-arelle/archive/0.2.2.tar.gz', # I'll explain this in a second
  keywords = ['arelle', 'lendflo', 'fork'], # arbitrary keywords
  classifiers = [],
)