from django.shortcuts import render
from .models import Company
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
	return render(request,'main/home.html')


#panel de oshas
def oshas(request):
	return render(request,'main/oshas.html')


#panel de ley de seguridad ambiental
def law(request):
	#if user is admin 
	companies = Company.objects.all()
	#else 
		#companies = Company.objects.get(su empresa)
	return render(request, "main/ley_seguridad.html", locals())