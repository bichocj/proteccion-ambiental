from django.shortcuts import render, redirect #puedes importar render_to_response
from files.forms import UploadForm
from files.models import Document
  
def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
        	newdoc = Document(docfile = request.FILES['docfile'])
        	newdoc.save(form)
        	return redirect("home")
    else:
        form = UploadForm()
        return render(request, 'index.html', locals())