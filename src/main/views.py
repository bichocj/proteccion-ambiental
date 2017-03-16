from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404

from proteccion_ambiental.settings import COMPANY_JRA_SLUG
from .models import Company, Format, Requirement, HistoryFormats, Accident, Company_Requirement
from .forms import CompanyForm, FormatForm, AccidentForm, EmployeeForm, RequirementForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.translation import ugettext as _


@login_required
def home(request):
    company_jra_slug = COMPANY_JRA_SLUG
    return render(request, 'main/home.html', locals())


# panel de oshas
@login_required
def config(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, 'main/configuration.html', locals())


@login_required
def panel(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, 'main/panel.html', locals())


# panel de ley de seguridad ambiental
@login_required
def company_list(request):
    # if user is admin
    companias = Company.objects.all()
    # else
    # companies = Company.objects.get(su empresa)
    companies = list()
    for c in companias:
        if not c.slug == 'jra':
            companies.append(c)
    return render(request, "main/company/list.html", locals())


@login_required
def company_new(request):
    title = _('new company')
    if request.POST:
        company_form = CompanyForm(request.POST, request.FILES)
        employee_form = EmployeeForm(request.POST)
        if company_form.is_valid() and employee_form.is_valid():
            company = company_form.save()
            requirements = Requirement.objects.filter(type_requirement=Requirement.ENTERPRISE)
            for requirement in requirements:
                cr = Company_Requirement(company=company, requirement=requirement)
                cr.save()
                for f in requirement.format_set.filter(company=None):
                    hs = f.historyformats_set.all()
                    f.pk = None
                    f.company = company
                    f.save()
                    for h in hs:
                        h.pk = None
                        h.format = f
                        h.save()

            employee = employee_form.save(commit=False)
            employee.company = company
            employee.save()
            return redirect(reverse('main:company_list'))
        else:
            message = 'ERROR: Revise la informacion...!'
            return render(request, "main/company/form.html", locals())
    else:
        company_form = CompanyForm()
        employee_form = EmployeeForm()
    return render(request, "main/company/form.html", locals())


@login_required
def company_edit(request, company_slug):
    title = _('edit company')
    company = get_object_or_404(Company, slug=company_slug)
    if request.POST:
        update_action = request.GET.get('update')
        if update_action == 'company':
            company_form = CompanyForm(request.POST, request.FILES, instance=company)
            employee_form = EmployeeForm(instance=company.user)
            if company_form.is_valid():
                company = company_form.save()
                return redirect(reverse('main:company_list'))
        if update_action == 'contact':
            employee_form = EmployeeForm(request.POST, request.FILES, instance=company.user)
            company_form = CompanyForm(instance=company)
            if employee_form.is_valid():
                employee = employee_form.save()
                return redirect(reverse('main:company_list'))
    else:
        company_form = CompanyForm(instance=company)
        employee_form = EmployeeForm(instance=company.user)

    return render(request, "main/company/edit.html", locals())


@login_required
def format_list(request, company_slug, requirement_pk):
    company = get_object_or_404(Company, slug=company_slug)
    requirement = Requirement.objects.get(pk=requirement_pk)
    title = requirement.name
    formats = Format.objects.filter(company=company, requirement=requirement)
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
    return render(request, "main/requirements/formats/list.html", locals())


@login_required
def format_update(request, company_slug, requirement_pk, format_pk):
    company = get_object_or_404(Company, slug=company_slug)
    requirement = get_object_or_404(Requirement, pk=requirement_pk)
    format = get_object_or_404(Format, pk=format_pk, company=company)
    title = 'Requirement : {0} , updating format {1}'.format(requirement.name, format.name)

    if request.POST:
        form = FormatForm(request.POST, request.FILES, instance=format)
        if form.is_valid():
            history = HistoryFormats()
            history.format = format
            history.file = format.file
            history.save()
            form.save()
            return redirect(
                reverse('main:format_list', kwargs={"company_slug": company_slug, "requirement_pk": requirement_pk}))
    else:
        form = FormatForm(instance=format)
    return render(request, 'main/layout_form.html', locals())


@login_required
def requirements_list(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    requirements = list()
    for r in Company_Requirement.objects.filter(company=company.pk):
        requirements.append(r.requirement)
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
def config_requirements_list(request):
    requirements = Requirement.objects.filter(type_requirement=Requirement.ENTERPRISE)
    return render(request, 'main/config/requirements/list.html', locals())


@login_required
def config_requirement_format_list(request, requirement_pk):
    requirement = Requirement.objects.get(pk=requirement_pk)
    title = _('requirement') + ' : ' + requirement.name
    formats = Format.objects.filter(requirement=requirement, company=None)
    formats_pdf = list()
    formats_xlsx = list()
    if formats.count() > 0:
        for format in formats:
            if format.type_format == Format.PLANES:
                formats_pdf.append(format)
            else:
                formats_xlsx.append(format)
            format.form = FormatForm(instance=format)
            format.history = HistoryFormats.objects.filter(format=format)
    else:
        message = ' Usted no tiene formatos'
    return render(request, "main/config/requirements/formats/list.html", locals())


@login_required
def config_requirement_format_update(request, requirement_pk, format_pk):
    requirement = get_object_or_404(Requirement, pk=requirement_pk)
    format = get_object_or_404(Format, pk=format_pk)
    title = 'Requirement : {0} , updating format {1}'.format(requirement.name, format.name)

    if request.POST:
        form = FormatForm(request.POST, request.FILES, instance=format)
        if form.is_valid():
            history = HistoryFormats()
            history.format = format
            history.file = format.file
            history.save()

            form.save()

            return redirect(reverse('main:config_requirement_format_list', kwargs={"requirement_pk": requirement_pk}))
    else:
        form = FormatForm(instance=format)
    return render(request, 'main/layout_with_out_nav_form.html', locals())


@login_required
def config_requirement_format_new(request, requirement_pk):
    requirement = Requirement.objects.get(pk=requirement_pk)
    title = request.GET.get('title', '')
    title = '<b>Nuevo Formato</b> de {1} ,<br>para el requerimiento {0}'.format(requirement.name, title)

    if request.POST:
        form = FormatForm(request.POST, request.FILES)
        if form.is_valid():
            format = form.save(commit=False)
            format.requirement = requirement
            format.save()
        return redirect(
            reverse('main:config_requirement_format_list', kwargs={"requirement_pk": requirement_pk}))
    else:
        form = FormatForm()
    return render(request, 'main/layout_with_out_nav_form.html', locals())


@login_required
def requirement_new(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    title = 'new requirement'
    if request.POST:
        form = RequirementForm(request.POST)
        if form.is_valid():
            requirement = form.save()
            requirement.type_requirement = Requirement.PROTECTION
            requirement.save()
            cr = Company_Requirement(company=company, requirement=requirement)
            cr.save()
            return redirect(reverse('main:requirements_list', kwargs={"company_slug": company.slug}))
    else:
        form = RequirementForm()
        return render(request, 'main/layout_form.html', locals())


@login_required
def config_requirement_new(request):
    global_config = True
    if request.POST:
        form = RequirementForm(request.POST)
        if form.is_valid():
            requirement = form.save()
            requirement.type_requirement = Requirement.ENTERPRISE
            requirement.save()
            return redirect(reverse('main:config_requirements_list'))
    else:
        requirement_form = RequirementForm()
    return render(request, 'main/config/requirements/new.html', locals())


@login_required
def accident_list(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    accidents = Accident.objects.filter(company=company)
    return render(request, "main/accidents/list.html", locals())


@login_required
def format_new_other(request, company_slug, requirement_pk):
    company = get_object_or_404(Company, slug=company_slug)
    requirement = Requirement.objects.get(pk=requirement_pk)
    title = '<b>{0}:</b> Nuevo formato de Registros y Evidencias'.format(requirement.name)

    if request.POST:
        format = Format(company=company, requirement=requirement, file=request.FILES['file'])
        format.type_format = Format.REGISTERS
        format.save()
        return redirect(
            reverse('main:format_list', kwargs={"company_slug": company_slug, "requirement_pk": requirement_pk}))
    else:
        form = FormatForm()
        return render(request, 'main/layout_form.html', locals())


@login_required
def format_new(request, company_slug, requirement_pk):
    company = get_object_or_404(Company, slug=company_slug)
    requirement = get_object_or_404(Requirement, pk=requirement_pk)
    title = request.GET.get('title', '')
    title = '<b>Nuevo Formato</b> de {1} ,<br>para el requerimiento {0}'.format(requirement.name, title)

    if request.POST:
        form = FormatForm(request.POST, request.FILES)
        if form.is_valid():
            format = form.save(commit=False)
            format.requirement = requirement
            format.company = company
            format.save()
        return redirect(
            reverse('main:format_list', kwargs={"company_slug": company_slug, "requirement_pk": requirement_pk}))
    else:
        form = FormatForm()
    return render(request, 'main/layout_form.html', locals())


@login_required
def accident_edit(request, company_slug, accident_pk):
    company = get_object_or_404(Company, slug=company_slug)
    accident = Accident.objects.get(pk=accident_pk)
    title = 'editar accidente'
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
    form = AccidentForm(instance=accident)

    return render(request, "main/accidents/accidents.html", locals())


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
    return render(request, "main/accidents/accidents.html", locals())


@login_required
def agreement(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, "main/agreement.html", locals())


@login_required
def reports(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, "main/reports/reports.html", locals())
