# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from wcdb.models import Crises, People, Organizations, List_Item
from wcdb_ie import xml_reader, xml_etree2mods
import xml.etree.ElementTree as ET

def index(request):
	t = loader.get_template('wcdb/index.html')

	dummy = ET.ElementTree()
	f = open('tester.txt', 'w')
	tree = xml_reader("test.xml", f, dummy)
	tree = tree.getroot()
	xml_etree2mods(tree)

	peeps = People.objects.all()
	c = Context({'c' : peeps[0].name,})

	f.close()
	return HttpResponse(t.render(c))


"""
def static_two(request):
    return render_to_response('static2.html');

def static_three(request):
    return render_to_response('static3.html');

def static_four(request):
    return render_to_response('static4.html');

def static_five(request):
    return render_to_response('static5.html');

def static_six(request):
    return render_to_response('static6.html');

def static_seven(request):
    return render_to_response('static7.html');

def static_eight(request):
    return render_to_response('static8.html');

def static_nine(request):
    return render_to_response('static9.html');
"""
