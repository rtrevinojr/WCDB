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
from wcdb_ie import xml_validate
from models import People, Crises, Organizations, List_Item
import unittest

class SimpleTest(unittest.TestCase):
    def test_basic_addition(self):
        """

        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

    def test_static_page(self):
        from views import johnkerry
        self.assertTrue(type(johnkerry(None)) == HttpResponse)
        self.assertTrue(type(johnkerry(None).content) == str)
        self.assertTrue(johnkerry(None).content[0:23] == '<!DOCTYPE html>\n<html>\n')

    def test_static_page_many(self):
        from views import asean
        self.assertTrue(type(asean(None)) == HttpResponse)
        self.assertTrue(type(asean(None).content) == str)
        from views import bnpparibas
        self.assertTrue(type(bnpparibas(None)) == HttpResponse)
        self.assertTrue(type(bnpparibas(None).content) == str)
        from views import chinamaritime
        self.assertTrue(type(chinamaritime(None)) == HttpResponse)
        self.assertTrue(type(chinamaritime(None).content) == str)
        from views import humantrafficking
        self.assertTrue(type(humantrafficking(None)) == HttpResponse)
        self.assertTrue(type(humantrafficking(None).content) == str)
        from views import johnkerry
        self.assertTrue(type(johnkerry(None)) == HttpResponse)
        self.assertTrue(type(johnkerry(None).content) == str)
        from views import mohamedmorsi
        self.assertTrue(type(mohamedmorsi(None)) == HttpResponse)
        self.assertTrue(type(mohamedmorsi(None).content) == str)
        from views import northkorea
        self.assertTrue(type(northkorea(None)) == HttpResponse)
        self.assertTrue(type(northkorea(None).content) == str)
        from views import polaris
        self.assertTrue(type(polaris(None)) == HttpResponse)
        self.assertTrue(type(polaris(None).content) == str)
        from views import rickymartin
        self.assertTrue(type(rickymartin(None)) == HttpResponse)
        self.assertTrue(type(rickymartin(None).content) == str)

    def test_xml_validate(self) :
        xml = StringIO.StringIO("""
        <WorldCrisis>
          <Crisis>
            <Person></Person>
              <Organization></Organization>
              <Place></Place>
            </Crisis>
            <Crisis>
            <Unique>
              <Person></Person>
              <Organization></Organization>
              <Place><City></City></Place>
            </Unique>
          </Crisis>
        </WorldCrisis>
        """)
        result = xml_validate(xml, "")
        self.assertEqual(result, True)

    def test_tables_exist(self) :
        self.assertTrue(len(People.objects.all()) >= 0)
        self.assertTrue(len(Crises.objects.all()) >= 0)
        self.assertTrue(len(Organizations.objects.all()) >= 0)
        self.assertTrue(len(List_Item.objects.all()) >= 0)

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
    return result.getvalue()
