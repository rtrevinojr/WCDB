#!/usr/bin/python

import django
from models import Crises, Organizations, People, List_Item
import xml.etree.ElementTree as ET
import datetime
import time

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
	"""
	Helper method for xml_mods2etree().
	The first argument a Crisis/Person/Organization in the database.
	The second is its matching ElementTree node in the tree being formed.
	This method puts that element's Common data into the tree.
	"""
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
	"""
	Takes an ElementTree and returns a string representation.
	"""
	et = et.getroot()
	xml = []
	xml_etree2xml_helper(et, xml)
	return ''.join(xml)

def xml_etree2xml_helper (et, xml, tabs='') :
	"""
	Helper method for xml_etree2xml().
	Recursively converts a given node to XML.
	"""
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

def init_db () :
    
