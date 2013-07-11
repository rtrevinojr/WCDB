#!/usr/bin/python

import django
from wcdb.models import Crises, Organizations, People, List_Item
import xml.etree.ElementTree as ET
import datetime
import time
#from minixsv import pyxsval, xsvalErrorHandler


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
	xf.seek(0)
	try:
		pass #pyxsval.parseAndValidateXmlInputString(xf.read(), xsdText=sf.read())
	except xsvalErrorHandler.XsvalError as xe:
		# the file did not validate
		return False

	return True
	
def xml_reader (xf, sf):
	"""
	Takes in an xml file and stores
	the content in an ElementTree object
	xf is an XML file
	sf is an XML Schema file
	returns an ElementTree
	"""
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
		return 1

	xf.seek(0) # have to do this just cause
	
	try:
		et = ET.parse(xf)
	except Exception as e:
		# assuming syntax is not valid
		# once again tell the user that 
		# the import did not work
		return 2
	
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
			try :
				p = People.objects.get(idref=child.attrib["ID"])
			except People.DoesNotExist as dne :
				p = People()
				p.idref = child.attrib["ID"]

			# even if the person was created in the past, they should not have a name yet
			p.name = child.attrib["Name"]
		
			# fill in the other data 
			for gc in list(child) : 
				if gc.tag == "Kind" :
					p.kind = gc.text.strip()
				elif gc.tag == "Location" :
					p.location = gc.text.strip()
				elif gc.tag == "Organizations" :
					for ggc in list(gc) :
						o = Organizations.objects.get(idref=ggc.attrib["ID"])
						if o == None :
							o = Organizations()
							o.idref = ggc.attrib["ID"]
							o.save()
						p.save()
						p.organizations.add(o)
				elif gc.tag == "Common" :
					for ggc in gc :
						xml_etree2mods_common(p, ggc)
						
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
						try :
							o = Organizations.objects.get(idref=ggc.attrib["ID"])
						except Organizations.DoesNotExist as dne :
							o = Organizations()
							o.idref = ggc.attrib["ID"]
							o.save()
						c.save()
						c.organizations.add(o)
				elif gc.tag == "People" :
					for ggc in list(gc) :
						try :
							p = People.objects.get(idref=ggc.attrib["ID"])
						except People.DoesNotExist as dne :
							p = People()
							p.idref = ggc.attrib["ID"]
							p.save()
						c.save()
						c.people.add(p)
				elif gc.tag == "Locations" or gc.tag == "HumanImpact" or gc.tag == "EconomicImpact" or gc.tag == "ResourcesNeeded" or gc.tag == "WaysToHelp" : 
					List_Item.objects.filter(idref=c.idref,list_type=gc.tag).all().delete()
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
						li.save()

				elif gc.tag == "Common": 
					for ggc in gc :
						xml_etree2mods_common(c, ggc)

			c.save()
		
		# Read in an organization's data for our model
		elif child.tag == "Organization" :
			# Check to see if we have already created an instance of an organization
			try :
				o = Organizations.objects.get(idref=child.attrib["ID"])
			except Organizations.DoesNotExist as dne :
				o = Organizations()
				o.idref = child.attrib["ID"]
			
			# git the organization a name and its other attributes
			o.name = child.attrib["Name"]
			for gc in list(child) :
				if gc.tag == "Kind" :
					o.kind = gc.text.strip()
				elif gc.tag == "Location" :
					o.location = gc.text.strip()
				elif gc.tag == "History" or gc.tag == "ContactInfo" :
					List_Item.objects.filter(idref=o.idref,list_type=gc.tag).all().delete()
					for ggc in list(gc) :
						li = List_Item()
						li.idref = o.idref
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
						li.save()
				elif gc.tag == "Common" :
					for ggc in list(gc) :
						xml_etree2mods_common(o, ggc)

			o.save()

def xml_etree2mods_common (element, gc) :
	List_Item.objects.filter(idref=element.idref,list_type=gc.tag).all().delete()
	if gc.tag == "Summary" :
		element.summary = gc.text.strip()
	else :
		for ggc in list(gc) :		
			li = List_Item()
			li.idref = element.idref
			if ggc.text is not None :
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
			li.save()

def xml_mods2etree ():
	"""
	Takes all model instances and converts
	them to xml
	returns a string representing the xml
	"""
	
	# create an element tree for our data
	et = ET.ElementTree()

	# create a root which will be the global elem for the data
	root_elem = ET.Element("WorldCrises")

	# set the root of the element tree to the root_elem
	et._setroot(root_elem)



	# add the orgs table to the element tree
	for org in Organizations.objects.all() :
		organization_elem = ET.Element("Organization", { "ID" : org.idref, "Name" : org.name })
		
		# Add the org's common info to the element tree
		xml_mods2etree_common(org, organization_elem)

		#go through lists not in common
		uncommons = ["ContactInfo", "History"]
		for tag in uncommons :
			list_items = List_Item.objects.filter(idref=org.idref, list_type=tag)
			li_elem = ET.Element(tag)
			for li in list_items :
				temp_elem = ET.Element("li")
				if li.href is not None :
					temp_elem.attrib.update({"href" : li.href})
				if li.embed is not None :
					temp_elem.attrib.update({"embed" : li.embed})
				if li.text is not None :
					temp_elem.attrib.update({"text" : li.text})
				temp_elem.text = li.body
				li_elem.insert(0, temp_elem)
			organization_elem.insert(0, li_elem)

		# create and fill the people element for the organization 
		people_elem = ET.Element("People")
		orgs_people_list = People.objects.all()
		for person in orgs_people_list :
			if org in person.organizations.all() :
				temp_elem = ET.Element("Person", { "ID" : person.idref })
				people_elem.insert(0, temp_elem)
		organization_elem.insert(0, people_elem)

		# create and fill the crises element for the organization
		crisis_elem = ET.Element("Crises")
		orgs_crises_list = Crises.objects.all()
		for crisis in orgs_crises_list :
			if org in crisis.organizations.all() :
				temp_elem = ET.Element("Crisis", { "ID" : crisis.idref })
				crisis_elem.insert(0, temp_elem)
		organization_elem.insert(0, crisis_elem)

		root_elem.insert(0, organization_elem)



	# add the people table to the element tree
	people_list = People.objects.all()
	for per in people_list :
		person_elem = ET.Element("Person", { "ID" : per.idref, "Name" : per.name })

		# add the person's common elements to the element tree
		xml_mods2etree_common(per, person_elem)

		# add the persons location to the element tree
		location_elem = ET.Element("Location")
		location_elem.text = per.location
		person_elem.insert(0, location_elem)

		# add the kind of person to the element tree
		kind_elem = ET.Element("Kind")
		kind_elem.text = per.kind
		person_elem.insert(0, kind_elem)

		# create and fill the organizations element for the person
		org_elem = ET.Element("Organizations")
		for organization in per.organizations.all() :
			temp_elem = ET.Element("Org", { "ID" : organization.idref })
			org_elem.insert(0, temp_elem)	
		person_elem.insert(0, org_elem)

		# create and fill the crises element for the person
		crisis_elem = ET.Element("Crises")
		per_crises_list = Crises.objects.all()
		for crisis in per_crises_list :
			if per in crisis.people.all() :
				temp_elem = ET.Element("Crisis", { "ID" : crisis.idref })
				crisis_elem.insert(0, temp_elem)
		person_elem.insert(0, crisis_elem)

		root_elem.insert(0, person_elem)



	# add the crises table to the element tree
	crises_list = Crises.objects.all()
	for cr in crises_list :
		crisis_elem = ET.Element("Crisis", { "ID" : cr.idref, "Name" : cr.name })

		#go through all the list items that are in common
		xml_mods2etree_common(cr, crisis_elem)

		# go through all the list items that aren't common
		uncommons = ["WaysToHelp", "ResourcesNeeded", "EconomicImpact", "HumanImpact", "Locations"]
		for tag in uncommons :
			list_items = List_Item.objects.filter(idref=cr.idref, list_type=tag)
			li_elem = ET.Element(tag)
			for li in list_items :
				temp_elem = ET.Element("li")
				if li.href is not None :
					temp_elem.attrib.update({"href" : li.href})
				if li.embed is not None :
					temp_elem.attrib.update({"embed" : li.embed})
				if li.text is not None :
					temp_elem.attrib.update({"text" : li.text})
				temp_elem.text = li.body
				li_elem.insert(0, temp_elem)
			crisis_elem.insert(0, li_elem)

		# create the time element and add
		time_elem = ET.Element("Time")
		time_elem.text = str(cr.time)
		crisis_elem.insert(0, time_elem)

		# create the date element and add
		date_elem = ET.Element("Date")
		date_elem.text = str(cr.date)
		crisis_elem.insert(0, date_elem)

		# create the kind element and add
		kind_elem = ET.Element("Kind")
		kind_elem.text = cr.kind
		crisis_elem.insert(0, kind_elem)

		# create and fill the organizations element for the crisis
		org_elem = ET.Element("Organizations")
		for organization in cr.organizations.all() :
			temp_elem = ET.Element("Org", { "ID" : organization.idref })
			org_elem.insert(0, temp_elem)	

		crisis_elem.insert(0, org_elem)

		# create and fill the people element for the crisis
		people_elem = ET.Element("People")
		for person in cr.people.all() :
			temp_elem = ET.Element("Person", { "ID" : person.idref })
			people_elem.insert(0, temp_elem)	

		crisis_elem.insert(0, people_elem)

		# add the created crisis to the root
		root_elem.insert(0, crisis_elem)
	
	return et

def xml_mods2etree_common (db_entry, elem) :
	commons = ["Feeds", "Maps", "Videos", "Images", "ExternalLinks", "Citations"]
	common_elem = ET.Element("Common")
		
	# create the summary element and add
	summary_elem = ET.Element("Summary")
	summary_elem.text = db_entry.summary
	common_elem.insert(0, summary_elem)

	for tag in commons :
		list_items = List_Item.objects.filter(idref=db_entry.idref, list_type=tag)
		li_elem = ET.Element(tag)
		for li in list_items :
			temp_elem = ET.Element("li")
			if li.href is not None :
				temp_elem.attrib.update({"href" : li.href})
			if li.embed is not None :
				temp_elem.attrib.update({"embed" : li.embed})
			if li.text is not None :
				temp_elem.attrib.update({"text" : li.text})
			temp_elem.text = li.body
			li_elem.insert(0, temp_elem)
		common_elem.insert(0, li_elem)
	elem.insert(0, common_elem)

def xml_etree2xml (et):
	et = et.getroot()
	xml = []
	xml_etree2xml_helper(et, xml, '')
	return ''.join(xml)

def xml_etree2xml_helper (et, xml, tabs) :
	xml += tabs
	xml += '<'
	xml += et.tag
	if et.attrib is not None :
		for a in et.attrib :
			xml += ' '
			xml += a
			xml += '="'
			xml += et.attrib[a]
			xml += '"'
	xml += '>'
	if et.text is not None :
		xml += et.text
	haschildren = False
	for child in et :
		xml += '\n'
		xml_etree2xml_helper(child, xml, tabs + '\t')
		haschildren = True
	if haschildren:
		xml += '\n'
		xml += tabs
	xml += '</'
	xml += et.tag
	xml += ' >'

