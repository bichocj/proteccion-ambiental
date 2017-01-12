from django.shortcuts import render
from .models import Company, Format
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
	return render(request,'main/home.html')


#panel de oshas
@login_required
def panel(request, pk):
	company = Company.objects.get(pk = pk)
	return render(request,'main/panel.html', locals())


#panel de ley de seguridad ambiental
@login_required
def law(request):
	#if user is admin 
	companies = Company.objects.all()
	#else 
		#companies = Company.objects.get(su empresa)
	return render(request, "main/ley_seguridad.html", locals())

@login_required
def requeriment(request, pk):
	company = Company.objects.get(pk = pk)
	req_1 = Format.objects.filter(company = company, requeriments = 1)
	req_2 = Format.objects.filter(company = company, requeriments = 2)
	req_3 = Format.objects.filter(company = company, requeriments = 3)
	req_4 = Format.objects.filter(company = company, requeriments = 4)
	return render(request, "main/requeriment.html", locals())

@login_required
def calendar(request, pk):
	company = Company.objects.get(pk = pk)
	return render(request, "main/calendar.html", locals())

@login_required
def accidents(request, pk):
	company = Company.objects.get(pk = pk)
	return render(request, "main/accidents.html", locals())

@login_required
def agreement(request):
	return render(request, "main/agreement.html", locals())

@login_required
def reports(request, pk):
	company = Company.objects.get(pk = pk)
	return render(request, "main/reports.html", locals())


