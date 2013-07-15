# Create your views here.

def export_prompt (request) :
    return render_to_response('export_prompt.html')

def export_text (request) :
    return render_to_response('export_text.html')
