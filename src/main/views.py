# -*- coding: utf-8 -*-
import datetime
import json
from decimal import Decimal

from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _

from accounts.forms import WorkerForm
from indices.forms import IndexForm
from indices.models import Index, Index_Detail, ValuesDetail
from main.models import AccidentDetail, UserCompany, Worker
from proteccion_ambiental.settings import COMPANY_JRA_SLUG
from .forms import CompanyForm, FormatForm, AccidentForm, RequirementForm, LegalRequirementForm, \
    MedicControlForm, AccidentDetailForm, UserCompanyForm
from .models import Company, Format, Requirement, HistoryFormats, Accident, Company_Requirement, LegalRequirement, \
    MedicControl


@login_required
def home(request):
    company_jra_slug = COMPANY_JRA_SLUG
    user = request.user
    # try:
    #     employee = Employee.objects.get(user_ptr_id=user.pk)
    # except Employee.DoesNotExist:
    #     employee = None
    # show = False
    # show_all = False
    # if employee and employee.company.slug == company_jra_slug:
    #     show = True
    # if user.groups.filter(name="Doctor").exists():
    #     show_all = True
    return render(request, 'main/home.html', locals())


# panel de oshas
@login_required
def config(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)

    return render(request, 'main/configuration.html', locals())


@login_required
def panel(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    users = UserCompany.objects.filter(company=company)
    return render(request, 'main/panel.html', locals())


# panel de ley de seguridad ambiental
@login_required
def company_list(request):
    user = request.user
    if user.is_superuser:
        companies = Company.objects.exclude(slug=COMPANY_JRA_SLUG)
    else:
        user_company = UserCompany.objects.get(user=user)
        company = user_company.company
        companies = [company, ]

    return render(request, "main/company/list.html", locals())


@login_required
def company_new(request):
    title = _('Nueva Compañía')
    if request.POST:
        company_form = CompanyForm(request.POST, request.FILES)
        # employee_form = EmployeeForm(request.POST)
        if company_form.is_valid():  # and employee_form.is_valid():
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

            # employee = employee_form.save(commit=False)
            # employee.company = company
            # employee.save()
            return redirect(reverse('main:company_list'))
        else:
            message = 'ERROR: Revise la informacion...!'
            return render(request, "main/company/form.html", locals())
    else:
        company_form = CompanyForm()
        # employee_form = EmployeeForm()
    return render(request, "main/company/form.html", locals())


@login_required
def company_edit(request, company_slug):
    title = _('edit company')
    company = get_object_or_404(Company, slug=company_slug)
    if request.POST:
        update_action = request.GET.get('update')
        if update_action == 'company':
            company_form = CompanyForm(request.POST, request.FILES, instance=company)
            # employee_form = EmployeeForm(instance=company.user)
            if company_form.is_valid():
                company = company_form.save()
                return redirect(reverse('main:company_list'))
                # if update_action == 'contact':
            # employee_form = EmployeeForm(request.POST, request.FILES, instance=company.user)
            company_form = CompanyForm(instance=company)
            # if employee_form.is_valid():
            #     if company.user:
            #         employee = employee_form.save()
            #     else:
            #         employee = employee_form.save(commit=False)
            #         employee.company = company
            #         employee.save()
            #     return redirect(reverse('main:company_list'))
    else:
        company_form = CompanyForm(instance=company)
        # employee_form = EmployeeForm(instance=company.user)

    return render(request, "main/company/edit.html", locals())


@login_required
def format_list(request, company_slug, requirement_pk):
    company = get_object_or_404(Company, slug=company_slug)
    requirement = Requirement.objects.get(pk=requirement_pk)
    title = requirement.name
    formats = Format.objects.filter(company=company, requirement=requirement)

    domain = request.META['HTTP_HOST']
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
def indices(request, company_slug):
    company = Company.objects.get(slug=company_slug)
    edit = None
    indices = None
    success = False
    save_text = 'Guardar'
    try:
        indices = Index.objects.get(company=company)
        edit = True
    except Index.DoesNotExist:
        edit = False
    if not edit:
        if request.POST:
            form = IndexForm(request.POST)
            if form.is_valid():
                index = form.save(commit=False)
                index.company = company
                index.save()
                message = 'Se guardo sus indices'
                success = True
            else:
                message = 'Revisa la informacion'
        else:
            form = IndexForm()
    else:
        if request.POST:
            form = IndexForm(request.POST, instance=indices)
            if form.is_valid():
                form.save()
                message = 'Se actualizo sus indices'
                success = True
            else:
                message = 'Revisa la informacion'
        else:
            form = IndexForm(instance=indices)
    return render(request, 'main/indeces/list.html', locals())


@login_required
def medic_exam(request, company_slug):
    company = Company.objects.get(slug=company_slug)
    medic_controls = MedicControl.objects.filter(company=company)
    return render(request, 'main/medic_control/list.html', locals())


@login_required
def medic_exam_new(request, company_slug):
    title = 'Nuevo Control Medico'
    company = Company.objects.get(slug=company_slug)
    if request.POST:
        form = MedicControlForm(request.POST, request.FILES, company=company)
        if form.is_valid():
            medic_control = form.save(commit=False)
            medic_control.company = company
            medic_control.save()
            return redirect(reverse('main:medic_exam', kwargs={'company_slug': company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = MedicControlForm(company=company)
    return render(request, 'main/layout_form.html', locals())


@login_required
def medic_exam_edit(request, company_slug, medic_pk):
    title = 'Nuevo Control Medico'
    company = Company.objects.get(slug=company_slug)
    medic_control = MedicControl.objects.get(pk=medic_pk)
    if request.POST:
        form = MedicControlForm(request.POST, request.FILES, instance=medic_control, company=company)
        if form.is_valid():
            medic_control = form.save(commit=False)
            medic_control.company = company
            medic_control.save()
            return redirect(reverse('main:medic_exam', kwargs={'company_slug': company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = MedicControlForm(instance=medic_control, company=company)
    return render(request, 'main/layout_form.html', locals())


@login_required
def medic_exam_delete(request, company_slug, medic_pk):
    company = Company.objects.get(slug=company_slug)
    medic_control = MedicControl.objects.get(pk=medic_pk)
    medic_control.delete()
    return redirect(reverse('main:medic_exam', kwargs={'company_slug': company_slug}))


@login_required
def workers(request, company_slug):
    company = Company.objects.get(slug=company_slug)
    print('slug', company.slug)
    worker_view = True
    workers_company = Worker.objects.filter(company=company)
    return render(request, 'main/workers/list.html', locals())


@login_required
def worker_new(request, company_slug):
    title = 'Nuevo Trabajador Legal'
    company = Company.objects.get(slug=company_slug)
    if request.POST:
        form = WorkerForm(request.POST, request.FILES)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.company = company
            worker.date_out = None
            worker.save()
            return redirect(reverse('main:workers', kwargs={'company_slug': company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = WorkerForm()
    return render(request, 'main/layout_form.html', locals())


@login_required
def worker_record(request, company_slug, worker_pk):
    company = Company.objects.get(slug=company_slug)
    worker = Worker.objects.get(pk=worker_pk)
    year_actual = datetime.date.today().year
    numbers = list()
    pos = 0
    for key, value in Accident.TYPE_ACCIDENT_CHOICES:
        options = dict()
        options['one'] = Accident.objects.filter(Q(worker=worker), Q(type_accident=key),
                                                 Q(date__year=year_actual),
                                                 Q(date__month=1)).count()
        options['two'] = Accident.objects.filter(Q(worker=worker), Q(type_accident=key),
                                                 Q(date__year=year_actual),
                                                 Q(date__month=2)).count()
        options['three'] = Accident.objects.filter(Q(worker=worker), Q(type_accident=key),
                                                   Q(date__year=year_actual),
                                                   Q(date__month=3)).count()
        options['four'] = Accident.objects.filter(Q(worker=worker), Q(type_accident=key),
                                                  Q(date__year=year_actual),
                                                  Q(date__month=4)).count()
        options['five'] = Accident.objects.filter(Q(worker=worker), Q(type_accident=key),
                                                  Q(date__year=year_actual),
                                                  Q(date__month=5)).count()
        options['six'] = Accident.objects.filter(Q(worker=worker), Q(type_accident=key),
                                                 Q(date__year=year_actual),
                                                 Q(date__month=6)).count()
        options['seven'] = Accident.objects.filter(Q(worker=worker), Q(type_accident=key),
                                                   Q(date__year=year_actual),
                                                   Q(date__month=7)).count()
        options['eight'] = Accident.objects.filter(Q(worker=worker), Q(type_accident=key),
                                                   Q(date__year=year_actual),
                                                   Q(date__month=8)).count()
        options['nine'] = Accident.objects.filter(Q(worker=worker), Q(type_accident=key),
                                                  Q(date__year=year_actual),
                                                  Q(date__month=9)).count()
        options['ten'] = Accident.objects.filter(Q(worker=worker), Q(type_accident=key),
                                                 Q(date__year=year_actual),
                                                 Q(date__month=10)).count()
        options['eleven'] = Accident.objects.filter(Q(worker=worker), Q(type_accident=key),
                                                    Q(date__year=year_actual),
                                                    Q(date__month=11)).count()
        options['twelve'] = Accident.objects.filter(Q(worker=worker), Q(type_accident=key),
                                                    Q(date__year=year_actual),
                                                    Q(date__month=12)).count()
        options['pos'] = pos
        pos += 1
        print(options)
        numbers.append(options)
    return render(request, 'main/workers/record.html', locals())


@login_required
def worker_edit(request, company_slug, worker_pk):
    title = 'Editar Trabajador'
    company = Company.objects.get(slug=company_slug)
    worker = Worker.objects.get(pk=worker_pk)
    if request.POST:
        form = WorkerForm(request.POST, request.FILES, instance=worker)
        if form.is_valid():
            worker = form.save(commit=False)
            if worker.date_out == '':
                worker.date_out = None
            worker.save()
            return redirect(reverse('main:workers', kwargs={'company_slug': company.slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = WorkerForm(instance=worker)
    return render(request, 'main/layout_form.html', locals())


@login_required
def worker_delete(request, company_slug, worker_pk):
    company = Company.objects.get(slug=company_slug)
    worker = Worker.objects.get(pk=worker_pk)
    worker.delete()
    return redirect(reverse('main:workers', kwargs={'company_slug': company_slug}))


@login_required
def legal_requirement(request, company_slug):
    company = Company.objects.get(slug=company_slug)
    legal_requirements = LegalRequirement.objects.filter(entitie=company)
    return render(request, 'main/legal_requirement/list.html', locals())


@login_required
def legal_requirement_new(request, company_slug):
    title = 'Nuevo Requisito Legal'
    company = Company.objects.get(slug=company_slug)
    if request.POST:
        form = LegalRequirementForm(request.POST, request.FILES)
        if form.is_valid():
            legalRequirement = form.save(commit=False)
            legalRequirement.entitie = company
            legalRequirement.save()
            return redirect(reverse('main:legal_requirement', kwargs={'company_slug': company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = LegalRequirementForm()
    return render(request, 'main/layout_form.html', locals())


@login_required
def legal_requirement_edit(request, company_slug, requirement_pk):
    title = 'Editar Requisito Legal'
    company = Company.objects.get(slug=company_slug)
    legalRequirement = LegalRequirement.objects.get(pk=requirement_pk)
    if request.POST:
        form = LegalRequirementForm(request.POST, request.FILES, instance=legalRequirement)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:legal_requirement', kwargs={'company_slug': company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = LegalRequirementForm(instance=legalRequirement)
    return render(request, 'main/layout_form.html', locals())


@login_required
def legal_requirement_delete(request, company_slug, requirement_pk):
    company = Company.objects.get(slug=company_slug)
    legalRequirement = LegalRequirement.objects.get(pk=requirement_pk)
    legalRequirement.delete()
    return redirect(reverse('main:legal_requirement', kwargs={'company_slug': company_slug}))


@login_required
def format_update(request, company_slug, requirement_pk, format_pk):
    company = get_object_or_404(Company, slug=company_slug)
    requirement = get_object_or_404(Requirement, pk=requirement_pk)
    format = get_object_or_404(Format, pk=format_pk, company=company)
    title = 'Requirement : {0} , updating format {1}'.format(requirement.name, format.name)
    try:
        history = HistoryFormats.objects.filter(format=format)
        if history.count() <= 0:
            history = HistoryFormats()
            history.format = format
            history.file = format.file
            history.save()
    except HistoryFormats.DoesNotExist:
        history = HistoryFormats()
        history.format = format
        history.file = format.file
        history.save()
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
def config_indices_list(request):
    return render(request, 'main/config/indices/list.html')


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


def return_month(month):
    months = [{'mes': 'Enero', 'index': 1}, {'mes': 'Febrero', 'index': 2}, {'mes': 'Marzo', 'index': 3},
              {'mes': 'Abril', 'index': 4}, {'mes': 'Mayo', 'index': 5}, {'mes': 'Junio', 'index': 6},
              {'mes': 'Julio', 'index': 7},
              {'mes': 'Agosto', 'index': 8}, {'mes': 'Septiembre', 'index': 9}, {'mes': 'Octubre', 'index': 10},
              {'mes': 'Noviembre', 'index': 11}, {'mes': 'Diciembre', 'index': 12}]
    return months[int(month) - 1]


def validate_index(index):
    if index.sgsst:
        return False
    if index.legal:
        return False
    if index.icsst:
        return False
    if index.indice_no_conformidad:
        return False
    if index.medida_iperc:
        return False
    if index.liderazgo:
        return False
    if index.plan_contingencia:
        return False
    if index.mejora:
        return False
    if index.capacitacion:
        return False
    if index.personal_capacitado:
        return False
    if index.intensidad_formativa:
        return False
    if index.charlas:
        return False
    if index.incidentes:
        return False
    if index.inspecciones:
        return False
    if index.observaciones_planeadas:
        return False
    if index.auditorias:
        return False
    if index.simulacros_emergencia:
        return False
    if index.reconocimiento_trabajador:
        return False
    if index.engenieer:
        return False
    if index.first_auxi:
        return False
    if index.medic_atention:
        return False
    if index.lose_time:
        return False
    if index.fatal_accident:
        return False
    if index.frecuency:
        return False
    if index.severity:
        return False
    if index.accidentality:
        return False
    if index.professional_sick:
        return False
    if index.medic_exam:
        return False
    if index.ap_worker:
        return False
    if index.ap_worker_restric:
        return False
    if index.exposition:
        return False
    if index.monitoring:
        return False
    if index.medidas_control:
        return False
    return True


def restore_index(index):
    index.sgsst = None
    index.legal = None
    index.icsst = None
    index.indice_no_conformidad = None
    index.medida_iperc = None
    index.liderazgo = None
    index.plan_contingencia = None
    index.mejora = None
    index.capacitacion = None
    index.personal_capacitado = None
    index.intensidad_formativa = None
    index.charlas = None
    index.incidentes = None
    index.inspecciones = None
    index.observaciones_planeadas = None
    index.auditorias = None
    index.simulacros_emergencia = None
    index.reconocimiento_trabajador = None
    index.engenieer = None
    index.first_auxi = None
    index.medic_atention = None
    index.lose_time = None
    index.fatal_accident = None
    index.frecuency = None
    index.severity = None
    index.accidentality = None
    index.professional_sick = None
    index.medic_exam = None
    index.ap_worker = None
    index.ap_worker_restric = None
    index.exposition = None
    index.monitoring = None
    index.medidas_control = None
    index.save()
    return index


def restore_indices(request, company_slug, mounth):
    index = Index.objects.get(company__slug=company_slug)
    try:
        indices = Index_Detail.objects.get(index=index, mounth=mounth)
        indices = restore_index(indices)
    except Index_Detail.DoesNotExist:
        indices = Index_Detail(index=index, mounth=mounth)
        indices.save()
    return redirect(
        reverse('main:reports', kwargs={"company_slug": company_slug}))


def indices_update(request, company_slug, indice_slug):
    # company = get_object_or_404(Company, slug=company_slug)
    # index = Index.objects.get(company=company)
    # return http.HttpResponse(json.dumps(response), content_type="application/json")
    raise Http404


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
    title = 'Nuevo Requerimiento'
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
def requirement_edit(request, company_slug, requirement_pk):
    company = get_object_or_404(Company, slug=company_slug)
    company_requirement = Company_Requirement.objects.get(pk=requirement_pk)
    title = 'Editar Requerimiento'
    if request.POST:
        form = RequirementForm(request.POST, instance=company_requirement.requirement)
        if form.is_valid():
            requirement = form.save()
            return redirect(reverse('main:requirements_list', kwargs={"company_slug": company.slug}))
    else:
        form = RequirementForm(instance=company_requirement.requirement)
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
    accidents = Accident.objects.filter(company=company).order_by('-date')
    accident_view = True
    return render(request, "main/accidents/list.html", locals())


@login_required
def format_new_other(request, company_slug, requirement_pk):
    company = get_object_or_404(Company, slug=company_slug)
    requirement = Requirement.objects.get(pk=requirement_pk)
    title = '<b>{0}:</b> Nuevo formato de Registros y Evidencias'.format(requirement.name)

    if request.POST:
        format = Format(company=company, requirement=requirement, file=request.FILES['file'])
        format.type_format = Format.REGISTERS
        format.file.name = u'%s' % format.file.name

        history = HistoryFormats()
        history.format = format
        history.file = format.file
        history.save()

        format.save()
        return redirect(
            reverse('main:format_list', kwargs={"company_slug": company_slug, "requirement_pk": requirement_pk}))
    else:
        form = FormatForm()
        return render(request, 'main/layout_form.html', locals())


@login_required
def format_delete(request, company_slug, requirement_pk, format_pk):
    format = get_object_or_404(Format, pk=format_pk)
    format.delete()
    return redirect(reverse('main:format_list', kwargs={"company_slug": company_slug, "requirement_pk": requirement_pk}))

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
            history = HistoryFormats()
            history.format = format
            history.file = format.file
            history.save()

        return redirect(
            reverse('main:format_list', kwargs={"company_slug": company_slug, "requirement_pk": requirement_pk}))
    else:
        form = FormatForm()
    return render(request, 'main/layout_form.html', locals())


@login_required
def accident_edit(request, company_slug, accident_pk):
    company = get_object_or_404(Company, slug=company_slug)
    accident = Accident.objects.get(pk=accident_pk)
    details = AccidentDetail.objects.filter(accident=accident)
    title = 'editar accidente'
    if request.POST:
        form = AccidentForm(request.POST, request.FILES, instance=accident, user=request.user, company=company)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:accident_list', kwargs={"company_slug": company.slug}))
        else:
            message = 'Revise la informacion'
    form = AccidentForm(instance=accident, user=request.user, company=company)
    form_detail = AccidentDetailForm(company=company)
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
    title = 'NUEVO ACCIDENTES, INCIDENTES, ENFERMEDAD OCUPACIONAL Y ACTO INSEGURO'
    active_item_menu = 'accidents'
    if request.POST:
        form = AccidentForm(request.POST, request.FILES, user=request.user, company=company)
        form_detail = AccidentDetailForm(request.POST)
        if form.is_valid() and form_detail.is_valid():
            accident = form.save(commit=False)
            accident.company = company
            accident.save()
            detail = form_detail.save(commit=False)
            detail.accident = accident
            detail.save()
            return redirect(reverse('main:accident_list', kwargs={"company_slug": company.slug}))
        else:
            message = 'Review all information . . .'
    else:
        form = AccidentForm(user=request.user, company=company)
        form_detail = AccidentDetailForm(company=company)
    return render(request, "main/accidents/accidents.html", locals())


@login_required
def agreement(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, "main/agreement.html", locals())


def user_new(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    if request.POST:
        form = UserCompanyForm(request.POST)
        if form.is_valid():
            user = User(
                first_name=form.cleaned_data.get('first_name'),
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('username')
            )
            user.set_password(form.cleaned_data.get('password1'))
            group = Group.objects.get(pk=form.cleaned_data.get('group'))
            user.save()
            user.groups.add(group)
            user.save()
            user_company = UserCompany.objects.create(
                group=group,
                user=user,
                company=company)
            return redirect(reverse('main:panel', kwargs={'company_slug': company_slug}))
    else:
        form = UserCompanyForm()
    title = _('New user in %(company)s') % {'company': company.name}
    return render(request, 'main/layout_form.html', locals())


def user_delete(request, company_slug, pk):
    company = get_object_or_404(Company, slug=company_slug)
    user_company = get_object_or_404(UserCompany, pk=pk)
    user_company.delete()
    return redirect(reverse('main:panel', kwargs={'company_slug': company_slug}))

# def user_edit(request, company_slug, pk):
#     company = get_object_or_404(Company, slug=company_slug)
#     user_company = get_object_or_404(UserCompany, pk=pk)
#     if request.POST:
#         form = UserCompanyForm(request.POST)
#         if form.is_valid():
#             user = user_company.user
#             user.first_name = form.cleaned_data.get('first_name')
#             user.username = form.cleaned_data.get('username')
#             user.set_password(form.cleaned_data.get('password'))
#             user.save()
#
#             user_company.group = Group.objects.get(pk=form.cleaned_data.get('group')),
#             user_company.save()
#
#             return redirect(reverse('main:panel', kwargs={'company_slug': company_slug}))
#     else:
#         form = UserCompanyForm(
#             {
#                 'first_name': user_company.user.first_name,
#                 'username': user_company.user.username,
#                 'group': user_company.group,
#              }
#         )
#     title = _('Edit user in %(company)s') % {'company': company.name}
#     return render(request, 'main/layout_form.html', locals())
