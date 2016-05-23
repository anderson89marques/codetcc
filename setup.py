import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_chameleon',
    'pyramid_jinja2',
    'psycopg2',
    'pyramid_tm',
    'SQLAlchemy',
    'SQLAlchemy_Enum34',
    'transaction',
    'zope.sqlalchemy',
    'gunicorn',
    'paginate',
    'pyramid_debugtoolbar',
    'waitress',
    ]

setup(name='codetcc',
      version='0.0',
      description='codetcc',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='codetcc',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = codetcc:main
      [console_scripts]
      initialize_codetcc_db = codetcc.scripts.initializedb:main
      """,
      )
