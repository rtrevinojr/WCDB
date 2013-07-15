# Create your views here.
from django.shortcuts import render_to_response

def export_prompt (request) :
    return render_to_response('export_prompt.html')

def export_text (request) :
    return render_to_response('export_text.html')
