import unittest

if __name__ == '__main__':
    all_tests = unittest.TestLoader().discover('./tests', pattern='*_tests.py')
    unittest.TextTestRunner(verbosity=2).run(all_tests)
