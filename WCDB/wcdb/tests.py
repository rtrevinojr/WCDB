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
from django.conf import settings
from wcdb_ie import xml_validate, xml_reader, xml_etree2mods, xml_mods2etree, xml_etree2xml
from models import People, Crises, Organizations, List_Item
import xml.etree.ElementTree as ET
import unittest

class SimpleTest(unittest.TestCase):

    def setUp(self):
        import MySQLdb
        db_connection = MySQLdb.connect(host='z', user='zlozano', passwd='Ml6BaCJP8y')
        cursor = db_connection.cursor()
        try :
            cursor.execute('DROP DATABASE IF EXISTS test_cs373_zlozano')
        except Warning as w:
            pass
        cursor.execute('CREATE DATABASE test_cs373_zlozano')
        sql = file('wcdb/makedb.sql', 'r').read()
        cursor.close()
        db_connection = MySQLdb.connect(host='z', user='zlozano', passwd='Ml6BaCJP8y', db='test_cs373_zlozano')
        cursor = db_connection.cursor()
        cursor.execute(sql)
        cursor.close()

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
        xml = StringIO.StringIO('''<WorldCrises><Crisis ID="CRI_EGYPTR" Name="Political Unrest in Egypt">
		<Kind>Political Unrest</Kind>
		<Date>2013-01-16</Date>
		<Time>06:00:00</Time>
		<Locations>
			<li>Egypt, Africa</li>
		</Locations>
		<HumanImpact>
			<li>Human deaths, political turmoil, economic hardships for the population in general.</li>
		</HumanImpact>
		<EconomicImpact>
			<li>Creates   complications for economic reform caused by previous regime fallout. If approved, the loan will come with strict conditions. In order to receive it, the IMF instead of collateral it will require that Egypt implement economic reforms usually in the form of the unpopular austerity measures to cut Egypt's deficit. This translates into a cut in spending on public benefits, social services and development projects. It also comes with an increase in taxes on items such as food, alcohol and cigarettes and petroleum derived products which also include gasoline and cause higher fees for public services including transportation.</li>
		</EconomicImpact>
		<ResourcesNeeded>
			<li>None used other than previous loans to help Egypt of previous political unrest.</li>
		</ResourcesNeeded>
		<WaysToHelp>
			<li>Still pending a $4.8 billion loan from the International Monetary Fund (IMF)</li>
		</WaysToHelp>
		<Common>
			<Images>
				<li embed="http://www.csmonitor.com/var/ezflow_site/storage/images/media/content/2012/6-25-12-mohamed-morsi/12947278-1-eng-US/6-25-12-Mohamed-Morsi_full_600.jpg" text="Morsi picture"/>
			</Images>
			<Videos>
				<li embed="http://www.youtube.com/watch?v=K9d_P58qMx4" text="Mohamed Morsi - president elect"/>
			</Videos>
		</Common>
	</Crisis></WorldCrises>''')
        emptystr = StringIO.StringIO('this breaks stuff')
        self.assertEqual(xml_validate(xml, emptystr), False)
        self.assertEqual(xml_validate(emptystr, xml), False)

        easyschema = StringIO.StringIO("""<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
    <xsd:element name="WorldCrises">
    </xsd:element>
</xsd:schema>""")
        self.assertTrue(xml_validate(xml, easyschema))
        self.assertEqual(xml_validate(emptystr, easyschema), False)

        self.assertTrue(xml_validate(xml, file('Schema.xsd.xml', 'r')))

    def test_tables_exist(self) :
        self.assertTrue(len(People.objects.all()) >= 0)
        self.assertTrue(len(Crises.objects.all()) >= 0)
        self.assertTrue(len(Organizations.objects.all()) >= 0)
        self.assertTrue(len(List_Item.objects.all()) >= 0)

    def test_add_to_models(self) :
        xml = StringIO.StringIO('''<WorldCrises><Crisis ID="CRI_EGYPTR" Name="Political Unrest in Egypt">
		<Kind>Political Unrest</Kind>
		<Date>2013-01-16</Date>
		<Time>06:00:00</Time>
		<Locations>
			<li>Egypt, Africa</li>
		</Locations>
		<HumanImpact>
			<li>Human deaths, political turmoil, economic hardships for the population in general.</li>
		</HumanImpact>
		<EconomicImpact>
			<li>Creates   complications for economic reform caused by previous regime fallout. If approved, the loan will come with strict conditions. In order to receive it, the IMF instead of collateral it will require that Egypt implement economic reforms usually in the form of the unpopular austerity measures to cut Egypt's deficit. This translates into a cut in spending on public benefits, social services and development projects. It also comes with an increase in taxes on items such as food, alcohol and cigarettes and petroleum derived products which also include gasoline and cause higher fees for public services including transportation.</li>
		</EconomicImpact>
		<ResourcesNeeded>
			<li>None used other than previous loans to help Egypt of previous political unrest.</li>
		</ResourcesNeeded>
		<WaysToHelp>
			<li>Still pending a $4.8 billion loan from the International Monetary Fund (IMF)</li>
		</WaysToHelp>
		<Common>
			<Images>
				<li embed="http://www.csmonitor.com/var/ezflow_site/storage/images/media/content/2012/6-25-12-mohamed-morsi/12947278-1-eng-US/6-25-12-Mohamed-Morsi_full_600.jpg" text="Morsi picture"/>
			</Images>
			<Videos>
				<li embed="http://www.youtube.com/watch?v=K9d_P58qMx4" text="Mohamed Morsi - president elect"/>
			</Videos>
		</Common>
	</Crisis></WorldCrises>''')
        xml_etree2mods(xml_reader(xml, file('Schema.xsd.xml', 'r')).getroot())
        self.assertTrue(len(Crises.objects.all()) == 1)
        self.assertEqual(Crises.objects.get(idref='CRI_EGYPTR').kind, 'Political Unrest')
        self.assertEqual(List_Item.objects.get(idref='CRI_EGYPTR',list_type='Locations').body, 'Egypt, Africa')

    def test_get_from_models(self):
        xml = StringIO.StringIO('''<WorldCrises><Crisis ID="CRI_EGYPTR" Name="Political Unrest in Egypt">
		<Kind>Political Unrest</Kind>
		<Date>2013-01-16</Date>
		<Time>06:00:00</Time>
		<Locations>
			<li>Egypt, Africa</li>
		</Locations>
		<HumanImpact>
			<li>Human deaths, political turmoil, economic hardships for the population in general.</li>
		</HumanImpact>
		<EconomicImpact>
			<li>Creates   complications for economic reform caused by previous regime fallout. If approved, the loan will come with strict conditions. In order to receive it, the IMF instead of collateral it will require that Egypt implement economic reforms usually in the form of the unpopular austerity measures to cut Egypt's deficit. This translates into a cut in spending on public benefits, social services and development projects. It also comes with an increase in taxes on items such as food, alcohol and cigarettes and petroleum derived products which also include gasoline and cause higher fees for public services including transportation.</li>
		</EconomicImpact>
		<ResourcesNeeded>
			<li>None used other than previous loans to help Egypt of previous political unrest.</li>
		</ResourcesNeeded>
		<WaysToHelp>
			<li>Still pending a $4.8 billion loan from the International Monetary Fund (IMF)</li>
		</WaysToHelp>
		<Common>
			<Images>
				<li embed="http://www.csmonitor.com/var/ezflow_site/storage/images/media/content/2012/6-25-12-mohamed-morsi/12947278-1-eng-US/6-25-12-Mohamed-Morsi_full_600.jpg" text="Morsi picture"/>
			</Images>
			<Videos>
				<li embed="http://www.youtube.com/watch?v=K9d_P58qMx4" text="Mohamed Morsi - president elect"/>
			</Videos>
		</Common>
	</Crisis></WorldCrises>''')
        xml_etree2mods(xml_reader(xml, file('Schema.xsd.xml', 'r')).getroot())
        et = xml_mods2etree()
        self.assertEqual(type(et), type(ET.ElementTree('')))
        self.assertEqual(et.getroot().tag, 'WorldCrises')
        self.assertEqual(et.getroot()[0].tag, 'Crisis')
        self.assertEqual(len(et.getroot()), 1)
        etstring = xml_etree2xml(et)

class NoTestDbDatabaseTestRunner(DjangoTestSuiteRunner):
    #Override setup and teardown of databases to force test runner to work.

    def build_suite(self, test_labels, extra_tests=None, **kwargs) :
        return super(NoTestDbDatabaseTestRunner, self).build_suite(['wcdb'], extra_tests, **kwargs)

    def setup_databases(self, **kwargs):
        pass

    def teardown_databases(self, old_config, **kwargs):
        pass

def do_test():
    settings.RUNNING_OFF_TEST_DB = True
    result = StringIO.StringIO('')
    suite = unittest.TestLoader().loadTestsFromTestCase(SimpleTest)
    unittest.TextTestRunner(stream=result,verbosity=0).run(suite)
    settings.RUNNING_OFF_TEST_DB = False

    import MySQLdb
    db_connection = MySQLdb.connect(host='z', user='zlozano', passwd='Ml6BaCJP8y')
    cursor = db_connection.cursor()
    cursor.execute('DROP DATABASE IF EXISTS test_cs373_zlozano')

    return result.getvalue()

