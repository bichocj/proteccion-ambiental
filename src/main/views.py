from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .models import Company, Format, Requirement, HistoryFormats, Accident
from .forms import CompanyForm, FormatForm, AccidentForm, EmployeeForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required
def home(request):
    return render(request, 'main/home.html')


# panel de oshas
@login_required
def panel(request, company_pk):
    company = Company.objects.get(pk=company_pk)
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
def format_list(request, requirement_pk):
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
            return redirect(reverse('main:format_list', kwargs={'requirement_pk': format.requirement.pk}))
        except:
            return redirect(reverse('main:format_list', kwargs={'requirement_pk': format.requirement.pk}))

    else:
        requirement = Requirement.objects.get(pk=requirement_pk)
        title = requirement.name
        formats = Format.objects.filter(requirement=requirement)
        formats_pdf = list()
        formats_xlsx = list()
        if formats.count() != 0:
            for format in formats:
                if format.file.name.endswith('.pdf'):
                    formats_pdf.append(format)
                else:
                    formats_xlsx.append(format)
                format.form = FormatForm(instance=format)
                format.history = HistoryFormats.objects.filter(format=format)
        else:
            message = ' Usted no tiene formatos'
        return render(request, "main/requirements/format.html", locals())


@login_required
def requirements_list(request, pk):
    if request.POST:
        try:
            format = Format.objects.get(pk=pk)
            history = HistoryFormats()
            history.format = format
            history.document = format.document
            history.date_time = timezone.now()
            history.save()
            format.document = request.FILES['document']
            format.save()
            return redirect(reverse('main:requirements_list', kwargs={'pk': format.company.pk}))
        except KeyError:
            return redirect(reverse('main:requirements_list', kwargs={'pk': format.company.pk}))
    else:
        company = Company.objects.get(pk=pk)
        requirements = Requirement.objects.filter(is_active=True).order_by('order')
        for requirement in requirements:
            requirement.formats = Format.objects.filter(requirement__pk=requirement.pk,
                                                        company__pk=request.user.company.pk)
            for format in requirement.formats:
                format.form = FormatForm(instance=format)
                format.history = HistoryFormats.objects.filter(format=format)


def requirements_list(request, company_pk):
    company = Company.objects.get(pk=company_pk)
    requirements = Requirement.objects.filter(is_active=True).order_by('order')
    return render(request, "main/requirements/list.html", locals())


@login_required
def calendar_service(request, company_pk):
    company = Company.objects.get(pk=company_pk)
    return render(request, "main/calendars/service.html", locals())


@login_required
def calendar_training(request, company_pk):
    company = Company.objects.get(pk=company_pk)
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
            return redirect(reverse('main:law'))
    else:
        company_form = CompanyForm()
        employee_form = EmployeeForm()
    return render(request, "main/company/form.html", locals())


@login_required
def accident_list(request, company_pk):
    accidents = Accident.objects.filter(company=company_pk)
    return render(request, "main/accidents/list.html", locals())


@login_required
def accident_edit(request, accident_pk):
    accident = Accident.objects.get(pk=accident_pk)
    if request.POST:
        form = AccidentForm(request.POST, request.FILES)
        if form.is_valid():
            accident.title=form.instance.title
            accident.content=form.instance.content
            accident.type_accident=form.instance.type_accident
            accident.date=form.instance.date
            accident.evidence =form.files['evidence']
            accident.save()
            return redirect(reverse('main:accident_list', kwargs={"company_pk": accident.company.pk}))
        return redirect(reverse('main:accident_list', kwargs={"company_pk": accident.company.pk}))
    form = AccidentForm({'title':accident.title, 'content':accident.title, 'type_accident':accident.type_accident, 'date':accident.date})
    if form.is_valid():
        return render(request, "main/layout_form.html", locals())
    else:
        message = 'ERROR: Bad Request ... !'
        return redirect(reverse('main:accident_list', kwargs={"company_pk": accident.company.pk}))

@login_required
def accident_delete(request, accident_pk):
    if request.POST:
        return render(request, "main/accidents/list.html", locals())

    accident = Accident.objects.get(pk=accident_pk)
    if not accident is None:
        accident.delete()
        return redirect(reverse('main:accident_list', kwargs={"company_pk": accident.company.pk}))
    else:
        message = 'ERROR: Bad Request ... !'
        return redirect(reverse('main:accident_list', kwargs={"company_pk": accident.company.pk}))

@login_required
def accident_new(request, company_pk):
    title = 'nuevo accidente'
    active_item_menu = 'accidents'
    company = Company.objects.get(pk=company_pk)
    if request.POST:
        form = AccidentForm(request.POST, request.FILES)
        if form.is_valid():
            accident = form.save(commit=False)
            accident.company = company
            accident.save()
            return redirect(reverse('main:accident_list', kwargs={"company_pk": company.pk}))
        else:
            message = 'Review all information . . .'
    else:
        form = AccidentForm()
    return render(request, "main/layout_form.html", locals())


@login_required
def agreement(request):
    return render(request, "main/agreement.html", locals())


@login_required
def reports(request, company_pk):
    company = Company.objects.get(pk=company_pk)
    return render(request, "main/reports.html", locals())
