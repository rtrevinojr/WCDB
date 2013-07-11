from django.template import Context, loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from wcdb.models import Crises, People, Organizations, List_Item
from wcdb.forms import LoginForm, UploadFileForm
from wcdb_ie import xml_reader, xml_etree2mods, xml_mods2etree, xml_etree2xml
import xml.etree.ElementTree as ET
from django.shortcuts import render_to_response

from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth import authenticate, login

def index(request):
	return render_to_response('wcdb/index.html')
	"""
	t = loader.get_template('wcdb/index.html')

	if request.user.is_authenticated() :
		dummy = ET.ElementTree()
		f = open('tester.txt', 'w')
		tree = xml_reader("test.xml", f)
		tree = tree.getroot()
		xml_etree2mods(tree)

		db_tree = xml_mods2etree()

		f.write(db_tree.getroot().tag + "\n")
		for c in list(db_tree.getroot()) :
			f.write(c.tag + " " +  str(c.attrib) + "\n")
		f.write(xml_etree2xml(db_tree))

		peeps = People.objects.all()
		crises = Crises.objects.all()
		orgs = Organizations.objects.all()
		c = Context({'p' : peeps, 'c' : crises, 'o' : orgs, })

		f.close()
		return HttpResponse(t.render(c))
	else :
		return render(request, 'wcdb/login.html')
	"""

def my_login(request) :
	user =""
	if request.method == 'POST' :
		form = LoginForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None :
			if user.is_active :
				login(request, user)
				return render(request, 'wcdb/index.html')
			else :
				return HttpResponse("user not valid")
				# disabled
		else :
			return HttpResponse("login failed")
			# invalid login error
	elif request.user.is_authenticated() :
		return render(request, 'wcdb/index.html')

def import_file(request) :
	t = loader.get_template('wcdb/import.html')
	if request.method == 'POST' :
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid() :
			# handle_uploaded_file(request.FILES['file'])
			# we may want to handle this from a separate file ?
			xml = request.FILES["upload"]
			xsd = open("WorldCrises.xsd.xml", 'r')
			et = xml_reader(xml, xsd)
			if (et == 1):
				# xml is not valid against schema
				success = 1
			elif (et == 2):
				success = 2
			else: # et is an ElementTree
				xml_etree2mods(et.getroot())
				success = 0
			c = RequestContext(request, {'success': success})
			return HttpResponse(t.render(c))
	else :
		form = UploadFileForm()
	#return render_to_response('wcdb/import.html', {'form' : form})
	c = RequestContext(request)
	return HttpResponse(t.render(c))
	
	"""
	# template for the upload form page
	t = loader.get_template('wcdb/import.html')
	# template for the landing page for a successful upload
	if request.method == 'POST':
		xml = request.FILES["xml"]
		xsd = open("/u/tbc399/Documents/cs373/p3/cs373-wcdb/WCDB/WorldCrises.xsd.xml", 'r')
		et = xml_reader(xml, xsd)
		if (et == 1):
			# xml is not valid against schema
			success = 1
		elif (et == 2):
			success = 2
		else: # et is an ElementTree
			xml_etree2mods(et.getroot())
			success = 0
		c = RequestContext(request, {'success': success})
		return HttpResponse(t.render(c))

	c = RequestContext(request)
	return HttpResponse(t.render(c))
	"""

def export_file (request):
	et = xml_mods2etree()
	xml_string = xml_etree2xml(et)
	t = loader.get_template('wcdb/export.html')
	c = Context({'xml_text': xml_string})
	return HttpResponse(t.render(c))


from tests import do_test
def run_tests(request):
    do_test()
    return render_to_response('wcdb/test.html', {'result' : do_test()});
    

def static_two(request):
    return render_to_response('wcdb/static2.html');

def chinamaritime(request):
    return render_to_response('wcdb/China_Maritime_Conflict_page.html');

def humantrafficking(request):
    return render_to_response('wcdb/Human_Trafficking_page.html');

def northkorea(request):
    return render_to_response('wcdb/North_Korean_Conflict_page.html');

def johnkerry(request):
    return render_to_response('wcdb/John_Kerry_page.html');

def mohamedmorsi(request):
    return render_to_response('wcdb/Mohamed_Morsi_page.html');

def rickymartin(request):
    return render_to_response('wcdb/Ricky_Martin_page.html');

def asean(request):
    return render_to_response('wcdb/ASEAN_page.html');

def bnpparibas(request):
    return render_to_response('wcdb/BNP_Paribas_page.html');

def polaris(request):
    return render_to_response('wcdb/Polaris_Project_page.html');

"""
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
