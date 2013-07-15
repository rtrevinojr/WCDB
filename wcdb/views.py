# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse

def export_prompt (request) :
    return render_to_response('export_prompt.html', {'xml' : '<table>\n\t<nice things>\n\t\t<chocolate></chocolate>\n\t</nice things>\n</table>'})

def export_raw (request) :
    return render_to_response('export_raw.html', {'xml' : '<table>\n\t<nice things>\n\t\t<chocolate></chocolate>\n\t</nice things>\n</table>'})

def export_download(request) :
    response = HttpResponse('<table>\n\t<nice things>\n\t\t<chocolate></chocolate>\n\t</nice things>\n</table>', content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="ExportedXML.txt"'
    return response
