import sys
from os import path
import unittest

test_root = path.abspath(path.dirname(__file__) or '.')
sys.path.insert(0, test_root[:-5])

try:
    import flask
except ImportError:
    print('webapp requires the flask package to be installed.')
    sys.exit(1)

if __name__ == '__main__':
    print('Running webapp test suite...')
    all_tests = unittest.TestLoader().discover('.', pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(all_tests)
