# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from wcdb_ie import xml_mods2etree, xml_etree2xml

def export_prompt (request) :
    return render_to_response('export_prompt.html', {'xml' : get_exported_table()})

def export_raw (request) :
    return render_to_response('export_raw.html', {'xml' : get_exported_table()})

def export_download(request) :
    response = HttpResponse(get_exported_table(), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="ExportedXML.txt"'
    return response

def get_exported_table() :
    return '<table>\n\t<nice things>\n\t\t<chocolate></chocolate>\n\t</nice things>\n</table>'
