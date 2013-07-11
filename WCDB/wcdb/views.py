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
	t = loader.get_template('wcdb/index.html')
	
	if request.user.is_authenticated() :
		dummy = ET.ElementTree()
		f = open('tester.txt', 'w')
		tree = xml_reader("test.xml", f, dummy)
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

def upload_file(request) :
	if request.method == 'POST' :
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid() :
			# handle_uploaded_file(request.FILES['file'])
			# we may want to handle this from a separate file ?
			return HttpResponseRedirect('/wcdb/')
	else :
		form = UploadFileForm()
	return render_to_response('wcdb/upload.html', {'form' : form})



def static_two(request):
    return render_to_response('wcdb/static2.html');
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
