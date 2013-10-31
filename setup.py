try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages

import sys

requires = ['Flask>=0.10', 'SQLAlchemy>=0.8.2', 'pymysql3']

if sys.version_info < (3, 3):
    print('ERROR: Flask_Webapp requires at least Python 3.3 to run.')
    sys.exit(1)

setup(
    name="Flask_Webapp",
    version="0.1",
    packages=find_packages(),
    package_data = {
        'flask_webapp.webapp': ['*.cfg'],
    },
    entry_points={
        'console_scripts': [
            'flask_webapp-quickstart = flask_webapp.quickstart:main',
        ],
    },
    install_requires=requires,
    #test_suite='flask_webapp.tests.run'
)
