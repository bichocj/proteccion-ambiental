# -*- coding: utf-8 -*-
from _pydecimal import Decimal
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404, render

from acuerdos_sst.models import Agreement
from fullcalendar.models import Events, REALIZADO, CAPACITATION
from indices.models import Index, Index_Detail, ValuesDetail
from main.models import Company, LegalRequirement, Worker
from main.views import return_month
from django.utils.translation import ugettext as _


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


def monthly_report(request, company_slug, mes):
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


@login_required
def reports(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    # months = []
    current_date = datetime.now()
    months = [{'mes': '{}'.format(_(current_date.replace(month=i).strftime('%B'))), 'index': i} for i in range(1, 13)]
    year = datetime.now().year
    return render(request, "main/reports/reports.html", locals())
