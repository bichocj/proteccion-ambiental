from django.shortcuts import render
from django.contrib import messages 
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .forms import FormEntrada
from .models import Entrada

def Entrada(request):
	if request.method == 'POST':
		form = FormEntrada(request.POST, request.FILES)
		if form.is_valid():
			titulo = request.POST['titulo']
			texto = request.POST['texto']
			archivo = request.FILES['archivo']

			insert = Entrada(titulo = titulo, texto = texto, archivo = Archivo)
			insert.save()

			return render(request, 'index.html', locals())
		else:
			messages.error(request, "Error al procesar el formulario")
	else:
		return render(request,'index.html', locals())
