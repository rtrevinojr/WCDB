from xml.etree.ElementTree import Element, fromstring, tostring
from xml.dom import minidom

OUR_IDS =  ['CRI_CHINAD', 'CRI_SCMARI', 'CRI_NKCONF', 'CRI_FINCRI', 'CRI_HUMTRA',
                        'CRI_EGYPTR', 'CRI_AIDSHI', 'CRI_AZWILD', 'CRI_LRACON', 'CRI_OSLOSH',

                        'PER_MMORSI', 'PER_LALOCA', 'PER_GASPAR', 'PER_CYLUNG', 'PER_JKERRY',
                        'PER_BROBMA', 'PER_MAGICJ', 'PER_COPETE', 'PER_VPUTIN', 'PER_JEABEL', 'PER_JONGUN',

                        'ORG_MAMFDN', 'ORG_FIREDP', 'ORG_PARIBS', 'ORG_ASEANA', 'ORG_POLARS',
                        'ORG_IMFUND', 'ORG_UNINAT', 'ORG_RIBBON', 'ORG_SALARM', 'ORG_WHORGN']


# missing:
# CEO of TEPCO Masataka Shimizu
# American mechanical engineer Roger Boisjoly
# Russian President Vladimir Putin
# Joint United Nations Programme on HIV/AIDS (UNAIDS)


xmlfile = open('Whole.xml', 'r')
xmlfile.seek(0)
xml1 = xmlfile.read()
#print xml

def prune(xml):
        new_tree = Element('WorldCrises')
        for el in fromstring(xml1):
                if el.get('ID') in OUR_IDS:
                        new_el = fromstring(tostring(el))
                        remove_top_level = []
                        for child in new_el:
                                if child.tag in ['Crises', 'People', 'Organizations']:
                                        to_remove = []
                                        for link in child:
						#print link.get('ID')
                                                if link.get('ID') not in OUR_IDS:
                                                        to_remove.append(link)
                                        [child.remove(l) for l in to_remove]
                                        if not len(child):
                                                remove_top_level.append(child)
                        [new_el.remove(c) for c in remove_top_level]
                        new_tree.append(new_el)
        jacked =  minidom.parseString(tostring(new_tree)).toprettyxml()
        return '\n'.join(l for l in jacked.split('\n') if l.strip())

def prune_2(xml):
	"""original pruning function from aaron's repo"""
	new_tree = Element('WorldCrises')
	for el in fromstring(xml1):
		if el.get('ID').split('_')[-1] in OUR_IDS:
			new_el = fromstring(tostring(el))
			remove_top_level = []
			for child in new_el:
				if child.tag in ['Crises', 'People', 'Organizations']:
					to_remove = []
					for link in child:
						if link.get('ID')[4:] not in OUR_IDS:
							to_remove.append(link)
					[child.remove(l) for l in to_remove]
					if not len(child):
						remove_top_level.append(child)
			[new_el.remove(c) for c in remove_top_level]
			new_tree.append(new_el)
	jacked =  minidom.parseString(tostring(new_tree)).toprettyxml()
	return '\n'.join(l for l in jacked.split('\n') if l.strip())


result = prune(xml1)
#print result[22000: 22100]
filename = 'WCDB1.xml'
fileout = open(filename, 'w')

fileout.write(result.encode('utf8'))
print 'check for a file called %s.' % filename
print 'this is your pruned xml.'
