import shutil
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .models import Company, Format, Requirement, HistoryFormats
from .forms import CompanyForm, FormatForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def home(request):
    return render(request, 'main/home.html')




# panel de oshas
@login_required
def panel(request, pk):
    company = Company.objects.get(pk=pk)
    return render(request, 'main/panel.html', locals())


# panel de ley de seguridad ambiental
@login_required
def law(request):
    companies = Company.objects.all()
    return render(request, "main/ley_seguridad.html", locals())


@login_required
def format_list(request, pk):
    if request.POST:
        try:
            format = Format.objects.get(pk = pk)
            history = HistoryFormats()
            history.format = format
            history.file = format.file
            history.date_time = timezone.now()
            history.save()
            format.file = request.FILES['file']
            format.save()
            title = format.requirement.name
            return redirect(reverse('main:format_list', kwargs={'pk': format.requirement.pk}))
        except:
            return redirect(reverse('main:format_list', kwargs={'pk': format.requirement.pk}))

    else:
        requirement = Requirement.objects.get(pk = pk)
        title = requirement.name
        formats = Format.objects.filter(requirement = requirement)
        formats_pdf = list()
        formats_xlsx = list()
        if formats.count() != 0:
            for format in formats:
                if format.file.name.endswith('.pdf'):
                    formats_pdf.append(format)
                else:
                    formats_xlsx.append(format)
                format.form = FormatForm(instance=format)
                format.history = HistoryFormats.objects.filter(format = format)
        else:
            message= ' Usted no tiene formatos'
        return render(request, "main/requirements/format.html", locals())

@login_required
def requirements_list(request, pk):
    company = Company.objects.get(pk=pk)
    requirements = Requirement.objects.filter(is_active=True).order_by('order')
    return render(request, "main/requirements/list.html", locals())


@login_required
def calendar_service(request, pk):
    company = Company.objects.get(pk=pk)
    return render(request, "main/calendars/service.html", locals())

@login_required
def calendar_training(request, pk):
    company = Company.objects.get(pk=pk)
    return render(request, "main/calendars/trainings.html", locals())

@login_required
def new_company(request):
    title = "Nueva empresa"
    if request.POST:
        form = CompanyForm(request.POST)
        if form.is_valid():
            comp = Company.objects.get(ruc = ruc)
            formats = Format.objects.filter(company = comp)
            company = form.save()
            for f in formats:
                format = Format()
                format.requirement = f.requirement
                format.file = f.file
                format.company = company
                format.save()
        return redirect(reverse('main:law'))
    else:
        form = CompanyForm()
    return render(request, "main/hook/form.html", locals())



@login_required
def accidents(request, pk):
    company = Company.objects.get(pk=pk)
    return render(request, "main/accidents.html", locals())


@login_required
def agreement(request):
    return render(request, "main/agreement.html", locals())


@login_required
def reports(request, pk):
    company = Company.objects.get(pk=pk)
    return render(request, "main/reports.html", locals())
