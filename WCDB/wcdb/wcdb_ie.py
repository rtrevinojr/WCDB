#!/usr/bin/python

import django
from wcdb.models import Crises, Organizations, People, List_Item
import xml.etree.ElementTree as ET
import datetime
import time
#from minixsv import pyxsval


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
		# handle without crashing
		# maybe give the user a warning to 
		# try again
		sf.write("Fails in first try\n")
		return False

	"""
	if (not xml_validate(xf, sf)):
		# handle still without crashing
		# warn user that xml isn't valid
		return False
	"""	

	try:
		et = ET.parse(xf)
	except Exception as e:
		# assuming syntax is not valid
		# once again tell the user that 
		# the import did not work
		return False
	
	return et

def xml_etree2mods (et):
	"""
	Takes in an ElementTree and builds
	model instances from the elements
	et is an ElementTree
	returns void (for now. might need to return a list of instances)
	"""
	for child in list(et) :
		# Read in all of a person's data for our model
		if child.tag == "Person" :
			# look for a previously created instance of a person
			p = People.objects.get(idref=child.attrib["ID"])
			if p == None : 
				p = People()
				p.idref = child.attrib["ID"]

			# even if the person was created in the past, they should not have a name yet
			p.name = child.attrib["Name"]
		
			# fill in the other data 
			for gc in list(child) : 
				if gc.tag == "Kind" :
					p.kind = gc.text.strip()
				elif gc.tag == "Location" :
					p.location == gc.text.strip()
				elif gc.tag == "Organizations" :
					for ggc in list(gc) :
						o = Organizations.objects.get(idref=ggc.attrib["ID"])
						if o == None :
							o = Organizations()
							o.idref = ggc.attrib["ID"]
							o.save()
						p.save()
						p.organizations.add(o)
						
			p.save()

		# Read in a crisis's data for our model
		elif child.tag == "Crisis" :
			c = Crises()
			c.name = child.attrib["Name"]
			c.idref = child.attrib["ID"]	

			for gc in list(child) :
				if gc.tag == "Kind" :
					c.kind = gc.text.strip()
				elif gc.tag == "Date" :
					c.date = gc.text.strip()
				elif gc.tag == "Time" :
					temptime = gc.text.strip().split("+")
					c.time = datetime.datetime.strptime(temptime[0], "%H:%M:%S")
				elif gc.tag == "Organizations" :
					for ggc in list(gc) :
						o = Organizations.objects.get(idref=ggc.attrib["ID"])
						if o == None :
							o = Organizations()
							o.idref = ggc.attrib["ID"]
							o.save()
						c.save()
						c.organizations.add(o)
				elif gc.tag == "People" :
					for ggc in list(gc) :
						p = People.objects.get(idref=ggc.attrib["ID"])
						if p == None :
							p = People()
							p.idref = ggc.attrib["ID"]
							p.save()
						c.save()
						c.people.add(p)
				elif gc.tag == "Locations" or gc.tag == "HumanImpact" or gc.tag == "EconomicImpact" or gc.tag == "ResourcesNeeded" or gc.tag == "WaysToHelp" : 
					for ggc in list(gc) :
						li = List_Item()
						li.idref = c.idref
						li.body = ggc.text.strip()
						li.list_type = gc.tag
						try :
							li.href = ggc.attrib["href"]
						except KeyError:
							li.href = None
						try :
							li.embed = ggc.attrib["embed"]
						except KeyError:
							li.embed = None
						try :
							li.text = ggc.attrib["text"]
						except KeyError:
							li.text = None

				elif gc.tag == "Common": 
					for ggc in list(gc) :
						if ggc.tag == "Summary" :
							c.summary = ggc.text.strip()
						else : 
							for leaf in list(ggc) : 
								li = List_Item()
								li.idref = c.idref
								li.body = leaf.text.strip()
								li.list_type = ggc.tag
								try :
									li.href = leaf.attrib["href"]
								except KeyError:
									li.href = None
								try :
									li.embed = leaf.attrib["embed"]
								except KeyError:
									li.embed = None
								try :
									li.text = leaf.attrib["text"]
								except KeyError:
									li.text = None

			c.save()
		
		# Read in an organization's data for our model
		elif child.tag == "Organization" :
			# Check to see if we have already created an instance of an organization
			o = Organizations.objects.get(idref=child.attrib["ID"])
			if o == None : 
				o = Organizations()
				o.idref = child.attrib["ID"]
			
			# git the organization a name and its other attributes
			o.name = child.attrib["Name"]
			for gc in list(child) :
				if gc.tag == "Kind" :
					o.kind = gc.text.strip()
				elif gc.tag == "Location" :
					o.location = gc.text.strip()

			o.save()


def xml_mods2etree ():
	"""
	Takes all model instances and converts
	them to xml
	returns a string representing the xml
	"""
	pass

def xml_etree2xml (et):
	pass




