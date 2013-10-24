import sys
from os import path
import unittest

testroot = path.abspath(path.dirname(__file__) or '.')
sys.path.insert(0, testroot[:-5])

if __name__ == '__main__':
    all_tests = unittest.TestLoader().discover('.', pattern='test_*.py')
    unittest.TextTestRunner(verbosity=2).run(all_tests)
