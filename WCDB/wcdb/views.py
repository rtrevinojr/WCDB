# Create your views here.

from django.shortcuts import render_to_response

def static_one(request):
    return render_to_response('static1.html');

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
