# -*- coding: utf-8 -*-
import datetime
import json
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django import http

from accounts.forms import WorkerForm, WorkerEditForm
from acuerdos_sst.models import Agreement
from fullcalendar.models import Events, CAPACITATION, REALIZADO
from main.models import Worker, Employee, AccidentDetail
from indices.forms import IndexForm
from indices.models import Index, Index_Detail, ValuesDetail
from proteccion_ambiental.settings import COMPANY_JRA_SLUG
from .models import Company, Format, Requirement, HistoryFormats, Accident, Company_Requirement, LegalRequirement, \
    MedicControl
from .forms import CompanyForm, FormatForm, AccidentForm, EmployeeForm, RequirementForm, LegalRequirementForm, \
    MedicControlForm, AccidentDetailForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.translation import ugettext as _


@login_required
def home(request):
    company_jra_slug = COMPANY_JRA_SLUG
    user = request.user
    try:
        employee = Employee.objects.get(user_ptr_id=user.pk)
    except Employee.DoesNotExist:
        employee = None
    show = False
    show_all = False
    if employee and employee.company.slug == company_jra_slug:
        show = True
    if user.groups.filter(name="Doctor").exists():
        show_all = True
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
    user = request.user
    if user.is_superuser or User.objects.filter(pk=user.pk, groups__name='Doctor').exists():
        companias = Company.objects.all()
        companies = list()
        for c in companias:
            if not c.slug == COMPANY_JRA_SLUG:
                companies.append(c)
    else:
        employee = Employee.objects.get(user_ptr_id=user.pk)
        company = employee.company
        companies = list()
        companies.append(company)

    return render(request, "main/company/list.html", locals())


@login_required
def company_new(request):
    title = _('Nueva Compañía')
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
                if company.user:
                    employee = employee_form.save()
                else:
                    employee = employee_form.save(commit=False)
                    employee.company = company
                    employee.save()
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
        form = MedicControlForm(request.POST, request.FILES)
        if form.is_valid():
            medic_control = form.save(commit=False)
            medic_control.company = company
            medic_control.save()
            return redirect(reverse('main:medic_exam', kwargs={'company_slug': company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = MedicControlForm()
    return render(request, 'main/layout_form.html', locals())


@login_required
def medic_exam_edit(request, company_slug, medic_pk):
    title = 'Nuevo Control Medico'
    company = Company.objects.get(slug=company_slug)
    medic_control = MedicControl.objects.get(pk=medic_pk)
    if request.POST:
        form = MedicControlForm(request.POST, request.FILES, instance=medic_control)
        if form.is_valid():
            medic_control = form.save(commit=False)
            medic_control.company = company
            medic_control.save()
            return redirect(reverse('main:medic_exam', kwargs={'company_slug': company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = MedicControlForm(instance=medic_control)
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
        form = WorkerForm(request.POST)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.company = company
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
        form = WorkerEditForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            print(company_slug)
            return redirect(reverse('main:workers', kwargs={'company_slug': company.slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = WorkerEditForm(instance=worker)
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


def refresh_inform(request, company_slug, mes):
    company = Company.objects.get(slug=company_slug)
    month = return_month(mes)
    index, _ = Index.objects.get_or_create(company=company)
    index_detail, _ = Index_Detail.objects.get_or_create(index=index, mounth=month['index'])

    # is_empty_index = validate_index(index_detail)
    # display_restore_btn = 0
    # if request.user.is_superuser:
    #     display_restore_btn = 1

    if index.is_using_sgsst:
        denominator_sgsst = Events.objects.filter(Q(calendar__company=company),
                                                  Q(event_start__month=month['index'])).count()
        if not denominator_sgsst:
            denominator_sgsst = 0

        numerator_sgsst = Events.objects.filter(Q(calendar__company=company), Q(state=REALIZADO),
                                                Q(event_start__month=month['index'])).count()
        if not numerator_sgsst:
            numerator_sgsst = 0

        values, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='sgsst')

        values.numerator = numerator_sgsst
        values.denominator = denominator_sgsst
        values.save()

        index_detail.sgsst = Decimal(numerator_sgsst) * Decimal(100.00) / Decimal(denominator_sgsst)
        index_detail.save()

    if index.is_using_legal:
        denominator_legal = LegalRequirement.objects.filter(Q(entitie=company),
                                                            Q(datepublication__month=month['index'])).count()
        if not denominator_legal:
            denominator_legal = 0
        numerator_legal = LegalRequirement.objects.filter(Q(entitie=company), Q(state=LegalRequirement.CUMPLIO),
                                                          Q(datepublication__month=month['index'])).count()
        if not numerator_legal:
            numerator_legal = 0

        values, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='legal')

        values.numerator = numerator_legal
        values.denominator = denominator_legal
        values.save()
        if denominator_legal == 0:
            index_detail.legal = Decimal(0)
        else:
            index_detail.legal = Decimal(numerator_legal) * Decimal(100.00) / Decimal(denominator_legal)
        index_detail.save()

    if index.is_using_capacitacion:
        events = Events.objects.filter(event_start__month=month['index'], calendar__type=CAPACITATION)
        total = events.count()
        total_done = events.filter(state=REALIZADO).count()

        index_detail.capacitacion = total_done * 100 / total
        index_detail.save()

    if index.is_using_icsst:
        denominator_icsst = Agreement.objects.filter(Q(company=company),
                                                     Q(date__month=month['index'])).count()
        if not denominator_icsst:
            denominator_icsst = 0
        print(denominator_icsst)
        numerator_icsst = Agreement.objects.filter(Q(company=company), Q(percentage=Decimal(100.0)),
                                                   Q(date__month=month['index'])).count()
        if not numerator_icsst:
            numerator_icsst = 0
        try:
            values = ValuesDetail.objects.get(detail=index_detail, key='icsst')
        except:
            values = ValuesDetail(detail=index_detail, key='icsst')
        values.numerator = numerator_icsst
        values.denominator = denominator_icsst
        values.save()
        if denominator_icsst == 0:
            index_detail.icsst = Decimal(0)
        else:
            index_detail.icsst = Decimal(numerator_icsst) * Decimal(100.00) / Decimal(denominator_icsst)
        index_detail.save()
        # else:
        #     try:
        #         values = ValuesDetail.objects.get(detail=index_detail, key='icsst')
        #     except:
        #         values = ValuesDetail(detail=index_detail, key='icsst')
        #     numerator_icsst = values.numerator
        #     denominator_icsst = values.denominator
    if index.is_using_indice_no_conformidad:
        # if index_detail.indice_no_conformidad == 0:
        denominator_indice_no_conformidad = Agreement.objects.filter(Q(company=company),
                                                                     Q(date__month=month['index'])).count()
        if not denominator_indice_no_conformidad:
            denominator_indice_no_conformidad = 0
        print(denominator_indice_no_conformidad)
        numerator_indice_no_conformidad = Agreement.objects.filter(Q(company=company), Q(percentage=Decimal(100.0)),
                                                                   Q(date__month=month['index'])).count()
        if not numerator_indice_no_conformidad:
            numerator_indice_no_conformidad = 0
        try:
            values = ValuesDetail.objects.get(detail=index_detail, key='indice_no_conformidad')
        except:
            values = ValuesDetail(detail=index_detail, key='indice_no_conformidad')
        values.numerator = numerator_indice_no_conformidad
        values.denominator = denominator_indice_no_conformidad
        values.save()
        if denominator_indice_no_conformidad == 0:
            index_detail.indice_no_conformidad = Decimal(0)
        else:
            index_detail.indice_no_conformidad = Decimal(numerator_indice_no_conformidad) * Decimal(
                100.00) / Decimal(
                denominator_indice_no_conformidad)
        index_detail.save()
        # else:
        #     try:
        #         values = ValuesDetail.objects.get(detail=index_detail, key='indice_no_conformidad')
        #     except:
        #         values = ValuesDetail(detail=index_detail, key='indice_no_conformidad')
        #     numerator_indice_no_conformidad = values.numerator
        #     denominator_indice_no_conformidad = values.denominator
    if index.is_using_medida_iperc:
        # if index_detail.medida_iperc == 0:
        denominator_medida_iperc = Agreement.objects.filter(Q(company=company),
                                                            Q(date__month=month['index'])).count()
        if not denominator_medida_iperc:
            denominator_medida_iperc = 0
        print(denominator_medida_iperc)
        numerator_medida_iperc = Agreement.objects.filter(Q(company=company), Q(percentage=Decimal(100.0)),
                                                          Q(date__month=month['index'])).count()
        if not numerator_medida_iperc:
            numerator_medida_iperc = 0
        try:
            values = ValuesDetail.objects.get(detail=index_detail, key='medida_iperc')
        except:
            values = ValuesDetail(detail=index_detail, key='medida_iperc')
        values.numerator = numerator_medida_iperc
        values.denominator = denominator_medida_iperc
        values.save()
        if denominator_medida_iperc == 0:
            index_detail.medida_iperc = Decimal(0)
        else:
            index_detail.medida_iperc = Decimal(numerator_medida_iperc) * Decimal(100.00) / Decimal(
                denominator_medida_iperc)
        index_detail.save()
        # else:
        #     try:
        #         values = ValuesDetail.objects.get(detail=index_detail, key='medida_iperc')
        #     except:
        #         values = ValuesDetail(detail=index_detail, key='medida_iperc')
        #     numerator_medida_iperc = values.numerator
        #     denominator_medida_iperc = values.denominator
    if index.is_using_liderazgo:
        # if index_detail.liderazgo == 0:
        denominator_liderazgo = Agreement.objects.filter(Q(company=company),
                                                         Q(date__month=month['index'])).count()
        if not denominator_liderazgo:
            denominator_liderazgo = 0
        print(denominator_liderazgo)
        numerator_liderazgo = Agreement.objects.filter(Q(company=company), Q(percentage=Decimal(100.0)),
                                                       Q(date__month=month['index'])).count()
        if not numerator_liderazgo:
            numerator_liderazgo = 0
        try:
            values = ValuesDetail.objects.get(detail=index_detail, key='liderazgo')
        except:
            values = ValuesDetail(detail=index_detail, key='liderazgo')
        values.numerator = numerator_liderazgo
        values.denominator = denominator_liderazgo
        values.save()
        if denominator_liderazgo == 0:
            index_detail.liderazgo = Decimal(0)
        else:
            index_detail.liderazgo = Decimal(numerator_liderazgo) * Decimal(100.00) / Decimal(
                denominator_liderazgo)
        index_detail.save()
        # else:
        #     try:
        #         values = ValuesDetail.objects.get(detail=index_detail, key='liderazgo')
        #     except:
        #         values = ValuesDetail(detail=index_detail, key='liderazgo')
        #     numerator_liderazgo = values.numerator
        #     denominator_liderazgo = values.denominator
    if index.is_using_plan_contingencia:
        # if index_detail.plan_contingencia == 0:
        denominator_plan_contingencia = Agreement.objects.filter(Q(company=company),
                                                                 Q(date__month=month['index'])).count()
        if not denominator_plan_contingencia:
            denominator_plan_contingencia = 0
        print(denominator_plan_contingencia)
        numerator_plan_contingencia = Agreement.objects.filter(Q(company=company), Q(percentage=Decimal(100.0)),
                                                               Q(date__month=month['index'])).count()
        if not numerator_plan_contingencia:
            numerator_plan_contingencia = 0
        try:
            values = ValuesDetail.objects.get(detail=index_detail, key='plan_contingencia')
        except:
            values = ValuesDetail(detail=index_detail, key='plan_contingencia')
        values.numerator = numerator_plan_contingencia
        values.denominator = denominator_plan_contingencia
        values.save()
        if denominator_plan_contingencia == 0:
            index_detail.plan_contingencia = Decimal(0)
        else:
            index_detail.plan_contingencia = Decimal(numerator_plan_contingencia) * Decimal(100.00) / Decimal(
                denominator_plan_contingencia)
        index_detail.save()
        # else:
        #     try:
        #         values = ValuesDetail.objects.get(detail=index_detail, key='plan_contingencia')
        #     except:
        #         values = ValuesDetail(detail=index_detail, key='plan_contingencia')
        #     numerator_plan_contingencia = values.numerator
        #     denominator_plan_contingencia = values.denominator
    title = 'REPORTE MENSUAL SEGURIDAD Y SALUD OCUPACIONAL'
    date_now = datetime.date.today()
    return redirect(reverse('main:mensual_report', kwargs={'company_slug': company_slug, 'mes': mes}))


def mensual_report(request, company_slug, mes):
    workers = Worker.objects.all()
    if workers.count() > 100:
        indice_general = 1000000
    else:
        indice_general = 200000

    # if request.method == 'GET' or request.GET:
    #     return redirect(reverse('main:reports', kwargs={'company_slug': company_slug}))
    company = get_object_or_404(Company, slug=company_slug)
    month = return_month(mes)
    # month = return_month(request.POST['mes'])
    index, _ = Index.objects.get_or_create(company=company)
    index_detail, _ = Index_Detail.objects.get_or_create(index=index, mounth=month['index'])
    values_details = ValuesDetail.objects.filter(detail=index_detail)

    return render(request, 'main/reports/reports_mensual.html', locals())


def indices_update(request, company_slug, indice_slug):
    company = get_object_or_404(Company, slug=company_slug)
    index = Index.objects.get(company=company)
    try:
        indices = Index_Detail.objects.get(index=index, mounth=request.POST['month'])
    except Index_Detail.DoesNotExist:
        indices = Index_Detail(index=index, mounth=request.POST['month'])
        indices.save()
    response = dict()
    val = None
    numerator = request.POST['numerator']
    denominator = request.POST['denominator']
    try:
        values = ValuesDetail.objects.get(detail=indices, key=indice_slug)
    except ValuesDetail.DoesNotExist:
        values = ValuesDetail(detail=indices, key=indice_slug)
        values.save()
    values.numerator = numerator
    values.denominator = denominator
    values.save()
    print('hola', numerator, denominator)
    if 'sgsst' == indice_slug:
        if denominator == 0:
            indices.sgsst = Decimal(0)
        else:
            indices.sgsst = Decimal(numerator) * Decimal(100.0) / Decimal(denominator)
        indices.save()
        indices = Index_Detail.objects.get(index=index, mounth=request.POST['month'])
        val = indices.sgsst
        print(indices.sgsst)
    if 'legal' == indice_slug:
        if denominator == 0:
            indices.legal = Decimal(0)
        else:
            indices.legal = Decimal(numerator) * Decimal(100.0) / Decimal(denominator)
        indices.save()
        indices = Index_Detail.objects.get(index=index, mounth=request.POST['month'])
        val = indices.legal
        print(indices.legal)
    if 'icsst' == indice_slug:
        if denominator == 0:
            indices.icsst = Decimal(0)
        else:
            indices.icsst = Decimal(numerator) * Decimal(100.0) / Decimal(denominator)
        indices.save()
        indices = Index_Detail.objects.get(index=index, mounth=request.POST['month'])
        val = indices.icsst
        print(indices.icsst)
    if 'indice_no_conformidad' == indice_slug:
        if denominator == 0:
            indices.indice_no_conformidad = Decimal(0)
        else:
            indices.indice_no_conformidad = Decimal(numerator) * Decimal(100.0) / Decimal(denominator)
        indices.save()
        indices = Index_Detail.objects.get(index=index, mounth=request.POST['month'])
        val = indices.indice_no_conformidad
        print(indices.indice_no_conformidad)
    if 'medida_iperc' == indice_slug:
        if denominator == 0:
            indices.medida_iperc = Decimal(0)
        else:
            indices.medida_iperc = Decimal(numerator) * Decimal(100.0) / Decimal(denominator)
        indices.save()
        indices = Index_Detail.objects.get(index=index, mounth=request.POST['month'])
        val = indices.medida_iperc
        print(indices.medida_iperc)
    if 'liderazgo' == indice_slug:
        if denominator == 0:
            indices.liderazgo = Decimal(0)
        else:
            indices.liderazgo = Decimal(numerator) * Decimal(100.0) / Decimal(denominator)
        indices.save()
        indices = Index_Detail.objects.get(index=index, mounth=request.POST['month'])
        val = indices.liderazgo
        print(indices.liderazgo)
    if 'plan_contingencia' == indice_slug:
        if denominator == 0:
            indices.plan_contingencia = Decimal(0)
        else:
            indices.plan_contingencia = Decimal(numerator) * Decimal(100.0) / Decimal(denominator)
        indices.save()
        indices = Index_Detail.objects.get(index=index, mounth=request.POST['month'])
        val = indices.plan_contingencia
        print(indices.plan_contingencia)
    response['success'] = True
    response['val'] = str(val)
    return http.HttpResponse(json.dumps(response), content_type="application/json")


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
    accidents = Accident.objects.filter(company=company)
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
        form = AccidentForm(request.POST, request.FILES, instance=accident, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:accident_list', kwargs={"company_slug": company.slug}))
        else:
            message = 'Revise la informacion'
    form = AccidentForm(instance=accident, user=request.user)
    form_detail = AccidentDetailForm()
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
        form = AccidentForm(request.POST, request.FILES, user=request.user)
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
        form = AccidentForm(user=request.user)
        form_detail = AccidentDetailForm()
    return render(request, "main/accidents/accidents.html", locals())


@login_required
def agreement(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, "main/agreement.html", locals())


@login_required
def reports(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    months = [{'mes': 'Enero', 'index': 1}, {'mes': 'Febrero', 'index': 2}, {'mes': 'Marzo', 'index': 3},
              {'mes': 'Abril', 'index': 4}, {'mes': 'Mayo', 'index': 5}, {'mes': 'Junio', 'index': 6},
              {'mes': 'Julio', 'index': 7},
              {'mes': 'Agosto', 'index': 8}, {'mes': 'Septiembre', 'index': 9}, {'mes': 'Octubre', 'index': 10},
              {'mes': 'Noviembre', 'index': 11}, {'mes': 'Diciembre', 'index': 12}]
    year = datetime.datetime.now().year
    return render(request, "main/reports/reports.html", locals())
