# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db import DatabaseError
from wcdb.wcdb_export import xml_mods2etree, xml_etree2xml

def export_prompt (request) :
    return render_to_response('export_prompt.html', {'xml' : get_exported_table()})

def export_raw (request) :
    return render_to_response('export_raw.html', {'xml' : get_exported_table()})

def export_download(request) :
    response = HttpResponse(get_exported_table(), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="ExportedXML.txt"'
    return response

def get_exported_table() :
    try:
        return xml_etree2xml(xml_mods2etree())
    except DatabaseError:
        return "<TableNotInitialized>\n\t<ohno></ohno>\n</TableNotInitialized>"
