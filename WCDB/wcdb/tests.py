"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

#from django.test import TestCase
import unittest
from django.http import HttpResponse
from views import static_two

class SimpleTest(unittest.TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_static_view(self):
        self.assert_(type(static_two(None)) == HttpResponse)
        self.assert_(''.join(static_two(None).content) == 'skeleton static webpage the second\n')
        

from django.test.simple import DjangoTestSuiteRunner
class NoTestDbDatabaseTestRunner(DjangoTestSuiteRunner):
    #Override setup and teardown of databases to force test runner to work.

    def build_suite(self, test_labels, extra_tests=None, **kwargs) :
        return super(NoTestDbDatabaseTestRunner, self).build_suite(['wcdb'], extra_tests, **kwargs)

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass
