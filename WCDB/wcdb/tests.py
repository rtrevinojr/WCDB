"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

#from django.test import TestCase
import sys
import StringIO
from django.test.simple import DjangoTestSuiteRunner
from django.http import HttpResponse
import unittest

class SimpleTest(unittest.TestCase):
    def test_basic_addition(self):
        """

        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 3)
        

class NoTestDbDatabaseTestRunner(DjangoTestSuiteRunner):
    #Override setup and teardown of databases to force test runner to work.

    def build_suite(self, test_labels, extra_tests=None, **kwargs) :
        return super(NoTestDbDatabaseTestRunner, self).build_suite(['wcdb'], extra_tests, **kwargs)

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass

def do_test():
    result = StringIO.StringIO('')
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleTest)
    unittest.TextTestRunner(stream=result,verbosity=0).run(suite)

    print '****TEST OUTPUT****'
    print result.getvalue()
    print '****END  OUTPUT****'
    return result.getvalue()
