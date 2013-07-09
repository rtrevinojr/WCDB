#!/usr/bin/python

import django
from wcdb.models import Crises, Organizations, People, List_Item
import xml.etree.ElementTree as ET
from minixsv import pyxsval

"""
Create an import/export facility from the XML into the Django models and back using ElementTree.
The import facility must import from a file to the Django models.
It must be password protected.
It must not crash when given a bad file.
It must report an error if the XML being imported does not match the schema using MiniXsv.
The export facility must export from the Django models to the screen in a way that is recognizable as XML.
Hint: There is a way to set the HTTP Content-Type to be text/wcdb1.
Import/export data on only the ten crises, ten organizations, and ten people of the group.
"""

def xml_validate (xf, sf):
	"""
	Takes in an xml file and checkes it against
	a given XML Schema. Reports an error if not
	valid.
	xf is an XML file
	sf is an XML Schema file
	return true if xf validates
	"""

	try:
		pyxsval.parseAndValidateXmlInput(xf, xsdFile=sf)
	except XsvalError as xe:
		# the file did not validate
		return False

	return True

def xml_reader (xf, sf, et):
	"""
	Takes in an xml file and stores
	the content in an ElementTree object
	xf is an XML file
	sf is an XML Schema file
	returns an ElementTree
	"""

	try:
		f = open(xf, 'r')
	except IOError as e:
		pass
		# handle without crashing
		# maybe give the user a warning to 
		# try again
		return False
	"""
	if (not xml_validate(xf, sf)):
	pass
	# handle still without crashing
	# warn user that xml isn't valid
	return False
	"""

	try:
		et = ET.parse(xf)
	except:
		# assuming syntax is not valid
		# once again tell the user that 
		# the import did not work
		return False

	return True

def xml_etree2mods (et):
	"""
	Takes in an ElementTree and builds
	model instances from the elements
	et is an ElementTree
	returns void (for now. might need to return a list of instances)
	"""
	child = list(et)[0]
	if child.tag == "Person" :
		p = People()
		p.name = child.attrib["Name"]
		p.idref = child.attrib["ID"]
		p.save()


def xml_mods2etree ():
	"""
	Takes all model instances and converts
	them to xml
	returns a string representing the xml
	"""
	pass

def xml_etree2xml (et):
	pass



xml_read("test.xml", "", tree)
xml_etree2mods(tree)
