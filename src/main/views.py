from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404

from proteccion_ambiental.settings import COMPANY_TEMPLATE_RUC, COMPANY_JRA_SLUG
from .models import Company, Format, Requirement, HistoryFormats, Accident
from .forms import CompanyForm, FormatForm, AccidentForm, EmployeeForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def home(request):
    company_jra_slug = COMPANY_JRA_SLUG
    return render(request, 'main/home.html', locals())


# panel de oshas
@login_required
def panel(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, 'main/panel.html', locals())


# panel de ley de seguridad ambiental
@login_required
def company_list(request):
    # if user is admin
    companies = Company.objects.all()
    # else
    # companies = Company.objects.get(su empresa)
    return render(request, "main/company/list.html", locals())


@login_required
def format_list(request, company_slug, requirement_pk):
    company = get_object_or_404(Company, slug=company_slug)
    if request.POST:
        try:
            format = Format.objects.get(pk=requirement_pk)
            history = HistoryFormats()
            history.format = format
            history.file = format.file
            history.date_time = timezone.now()
            history.save()
            format.file = request.FILES['file']
            format.save()
            title = format.requirement.name
            return redirect(reverse('main:format_list', kwargs={'company_slug':company_slug,'requirement_pk': format.requirement.pk}))
        except:
            return redirect(reverse('main:format_list', kwargs={'company_slug':company_slug,'requirement_pk': format.requirement.pk}))

    else:
        requirement = Requirement.objects.get(pk=requirement_pk)
        title = requirement.name
        formats = Format.objects.filter(company=company,requirement=requirement)
        formats_pdf = list()
        formats_xlsx = list()
        if formats.count() != 0:
            for format in formats:
                if format.type_format == Format.PLANES:
                    formats_pdf.append(format)
                else:
                    formats_xlsx.append(format)
                format.form = FormatForm(instance=format)
                format.history = HistoryFormats.objects.filter(format=format)
        else:
            message = ' Usted no tiene formatos'
        return render(request, "main/requirements/formats/format.html", locals())


@login_required
def requirements_list(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    requirements = Requirement.objects.filter(is_active=True).order_by('order')
    return render(request, "main/requirements/list.html", locals())


@login_required
def calendar_service(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, "main/calendars/service.html", locals())


@login_required
def calendar_training(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, "main/calendars/trainings.html", locals())


@login_required
def company_new(request):
    title = "Nueva empresa"
    if request.POST:
        company_form = CompanyForm(request.POST)
        employee_form = EmployeeForm(request.POST)
        if company_form.is_valid() and employee_form.is_valid():
            comp = Company.objects.get(ruc=COMPANY_TEMPLATE_RUC)
            formats = Format.objects.filter(company=comp)
            company = company_form.save()
            for f in formats:
                format = Format()
                format.requirement = f.requirement
                format.file = f.file
                format.company = company
                format.save()
            employee = employee_form.save(commit=False)
            employee.company = company
            employee.save()
            return redirect(reverse('main:company_list'))
    else:
        company_form = CompanyForm()
        employee_form = EmployeeForm()
    return render(request, "main/company/form.html", locals())


@login_required
def accident_list(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    accidents = Accident.objects.filter(company=company)
    return render(request, "main/accidents/list.html", locals())


@login_required
def format_new_other(request, company_slug, requirement_pk):
    company = get_object_or_404(Company, slug=company_slug)
    requirement = Requirement.objects.get(pk=requirement_pk)
    is_other=True
    if request.POST:
        format=Format(company=company,requirement=requirement,file=request.FILES['file'])
        format.type_format=Format.REGISTERS
        format.save()
        return redirect(reverse('main:format_list', kwargs={"company_slug": company_slug,"requirement_pk":requirement_pk}))            
    else:
        form=FormatForm()
        return render(request, 'main/requirements/formats/new_format.html', locals())


@login_required
def format_new_pdf(request, company_slug, requirement_pk):
    company = get_object_or_404(Company, slug=company_slug)
    requirement = Requirement.objects.get(pk=requirement_pk)
    if request.POST:
        format=Format(company=company,requirement=requirement,file=request.FILES['file'])
        format.type_format=Format.PLANES
        format.save()
        return redirect(reverse('main:format_list', kwargs={"company_slug": company_slug,"requirement_pk":requirement_pk}))            
    else:
        form=FormatForm()
    return render(request, 'main/requirements/formats/new_format.html', locals())


@login_required
def accident_edit(request, company_slug, accident_pk):
    company = get_object_or_404(Company, slug=company_slug)
    accident = Accident.objects.get(pk=accident_pk)
    if request.POST:
        form = AccidentForm(request.POST, request.FILES)
        if form.is_valid():
            accident.title = form.instance.title
            accident.content = form.instance.content
            accident.type_accident = form.instance.type_accident
            accident.date = form.instance.date
            accident.evidence = form.files['evidence']
            accident.save()
            return redirect(reverse('main:accident_list', kwargs={"company_slug": accident.company.pk}))
        return redirect(reverse('main:accident_list', kwargs={"company_slug": accident.company.pk}))
    form = AccidentForm({'title': accident.title, 'content': accident.title, 'type_accident': accident.type_accident,
                         'date': accident.date})
    if form.is_valid():
        return render(request, "main/layout_form.html", locals())
    else:
        message = 'ERROR: Bad Request ... !'
        return redirect(reverse('main:accident_list', kwargs={"company_slug": accident.company.pk}))


@login_required
def accident_delete(request, company_slug, accident_pk):
    company = get_object_or_404(Company, slug=company_slug)
    if request.POST:
        return render(request, "main/accidents/list.html", locals())

    accident = Accident.objects.get(pk=accident_pk)
    if not accident is None:
        accident.delete()
        return redirect(reverse('main:accident_list', kwargs={"company_slug": accident.company.slug}))
    else:
        message = 'ERROR: Bad Request ... !'
        return redirect(reverse('main:accident_list', kwargs={"company_slug": accident.company.slug}))


@login_required
def accident_new(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    title = 'nuevo accidente'
    active_item_menu = 'accidents'
    if request.POST:
        form = AccidentForm(request.POST, request.FILES)
        if form.is_valid():
            accident = form.save(commit=False)
            accident.company = company
            accident.save()
            return redirect(reverse('main:accident_list', kwargs={"company_slug": company.slug}))
        else:
            message = 'Review all information . . .'
    else:
        form = AccidentForm()
    return render(request, "main/layout_form.html", locals())


@login_required
def agreement(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, "main/agreement.html", locals())


@login_required
def reports(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, "main/reports.html", locals())
