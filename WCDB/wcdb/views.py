# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from wcdb.models import Crises, People, Organizations, List_Item

def index(request):
	crises = Crises.objects.all()
	t = loader.get_template('wcdb/index.html')
	c = Context({'Our Crises:' : crises,})
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
