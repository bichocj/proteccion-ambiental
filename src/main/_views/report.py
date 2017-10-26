# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q, Sum
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.translation import ugettext as _

from acuerdos_sst.models import Agreement
from fullcalendar.models import Events, DONE, CAPACITATION, CHARLAS, OTRO, INSPECTION, SIMULATION
from improvements.models import Agreement as AgreementImprovement
from indices.models import Index, Index_Detail, ValuesDetail
from main.models import Company, LegalRequirement, Worker, CountWorker, Accident


def refresh_inform(request, company_slug, month):
    company = Company.objects.get(slug=company_slug)

    index, _ = Index.objects.get_or_create(company=company)
    index_detail, _ = Index_Detail.objects.get_or_create(index=index, mounth=month)

    count_worker = CountWorker.objects.get(month_year__month=month)
    workers_in_month = count_worker.workers
    hours_worked_in_month = count_worker.hours

    # is_empty_index = validate_index(index_detail)
    # display_restore_btn = 0
    # if request.user.is_superuser:
    #     display_restore_btn = 1

    if index.is_using_sgsst:
        denominator_sgsst = Events.objects.filter(Q(calendar__company=company),
                                                  Q(event_start__month=month)).count()

        numerator_sgsst = Events.objects.filter(Q(calendar__company=company), Q(state=DONE),
                                                Q(event_start__month=month)).count()
        if not numerator_sgsst:
            numerator_sgsst = 0

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='sgsst')

        value_detail.numerator = numerator_sgsst
        value_detail.denominator = denominator_sgsst
        value_detail.save()

        index_detail.sgsst = numerator_sgsst * 100 / denominator_sgsst
        # index_detail.save()

    if index.is_using_legal:
        denominator_legal = LegalRequirement.objects.filter(Q(entitie=company),
                                                            Q(datepublication__month=month)).count()
        numerator_legal = LegalRequirement.objects.filter(Q(entitie=company), Q(state=LegalRequirement.CUMPLIO),
                                                          Q(datepublication__month=month)).count()

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='legal')

        value_detail.numerator = numerator_legal
        value_detail.denominator = denominator_legal
        value_detail.save()
        if denominator_legal == 0:
            index_detail.legal = 0
        else:
            index_detail.legal = numerator_legal * 100.00 / denominator_legal
            # index_detail.save()

    if index.is_using_capacitacion:
        events = Events.objects.filter(calendar__company=company, event_start__month=month,
                                       calendar__type=CAPACITATION)

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='training')

        value_detail.numerator = events.filter(state=DONE).count()
        value_detail.denominator = events.count()
        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator * 100 / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_personal_capacitado:
        events = Events.objects.filter(calendar__company=company, event_start__month=month,
                                       calendar__type=CAPACITATION)

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='personal_training')

        events_training = events.filter(state=DONE, type_capacitations__isnull=False)
        events_training_total = events_training.count()
        events_training_workers = events_training.aggregate(Sum('number_workers'))['number_workers__sum']
        value_detail.denominator = workers_in_month

        if value_detail.denominator > 0:
            value_detail.numerator = events_training_total * events_training_workers / value_detail.denominator
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.numerator = 0
            value_detail.value = 0
        value_detail.save()

    if index.is_using_intensidad_formativa:
        hours_worked = \
            (Events.objects.filter(calendar__company=company, event_start__month=month, state=DONE).filter(
                Q(calendar__type=CAPACITATION) | Q(calendar__type=CHARLAS)).aggregate(Sum('hours_worked')))[
                'hours_worked__sum']

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='formative_intensity')
        value_detail.numerator = hours_worked * 100
        value_detail.denominator = workers_in_month

        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_charlas:
        events = Events.objects.filter(calendar__company=company, event_start__month=month,
                                       calendar__type=CHARLAS)
        traings_todo = events.count()
        trainings_done = events.filter(state=DONE).count()
        people_trained = (events.filter(state=DONE).aggregate(Sum('number_workers')))['number_workers__sum']
        people_to_training = (events.aggregate(Sum('number_workers')))['number_workers__sum']

        if people_trained is None:
            people_trained = 0

        if people_to_training is None:
            people_to_training = 0

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='security_talks')
        value_detail.numerator = trainings_done * people_trained * 100
        value_detail.denominator = traings_todo * people_to_training

        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_incidentes:

        workers_with_incidents = Accident.objects.filter(company=company, date__month=month).count()

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='incidents')
        value_detail.numerator = workers_with_incidents * 100
        value_detail.denominator = 30

        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_inspecciones:

        inspections = Events.objects.filter(calendar__company=company, event_start__month=month,
                                            type=INSPECTION)

        inspections_done = inspections.filter(state=DONE).count()
        inspections_todo = inspections.count()

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='inspections')
        value_detail.numerator = inspections_done * 100
        value_detail.denominator = inspections_todo

        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_observaciones_planeadas:

        observations = Events.objects.filter(calendar__company=company, event_start__month=month, type=OTRO)

        observations_done = observations.filter(state=DONE).count()
        observations_todo = observations.count()

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='observations')
        value_detail.numerator = observations_done * 100
        value_detail.denominator = observations_todo

        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_simulacros_emergencia:

        simulacrums = Events.objects.filter(calendar__company=company, event_start__month=month,
                                            type=SIMULATION)

        simulacrums_done = simulacrums.filter(state=DONE).count()
        simulacrums_todo = simulacrums.count()

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='simulacrum')
        value_detail.numerator = simulacrums_done * 100
        value_detail.denominator = simulacrums_todo

        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_simulacros_emergencia:

        simulacrums = Events.objects.filter(calendar__company=company, event_start__month=month,
                                            type=SIMULATION)

        simulacrums_done = simulacrums.filter(state=DONE).count()
        simulacrums_todo = simulacrums.count()

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='simulacrum')
        value_detail.numerator = simulacrums_done * 100
        value_detail.denominator = simulacrums_todo

        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_first_auxi:

        aids = Accident.objects.filter(company=company, date__month=month,
                                       type_accident=Accident.FIRST_AID).count()

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='first_aid')
        value_detail.numerator = aids * 200000  # N°Accidentes Primeros Auxilios Acum x 200 000
        value_detail.denominator = hours_worked_in_month  # Horas Hombre Trabajadas Acumuladas

        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_medic_atention:

        aids = Accident.objects.filter(company=company, date__month=month,
                                       type_accident=Accident.MEDIC_ATTENTION).count()

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='medic_attention')
        value_detail.numerator = aids * 200000  # N°Accidentes A. Medica Acum x 200 000
        value_detail.denominator = hours_worked_in_month  # Horas Hombre Trabajadas Acumuladas

        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_lose_time:

        aids = Accident.objects.filter(company=company, date__month=month,
                                       type_accident=Accident.AID_LOST).count()

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='aids_lost')
        value_detail.numerator = aids * 200000  # N°Accidentes con tiempo perdido x 200 000
        value_detail.denominator = hours_worked_in_month  # Horas Hombre Trabajadas Acumuladas

        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_fatal_accident:

        aids = Accident.objects.filter(company=company, date__month=month,
                                       type_accident=Accident.AID_FATAL).count()

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='aids_fatal')
        value_detail.numerator = aids * 200000  # N°Accidentes Fatal x 200 000
        value_detail.denominator = hours_worked_in_month  # Horas Hombre Trabajadas Acumuladas

        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_frecuency:
        aids = Accident.objects.filter(company=company, date__month=month,
                                       type_accident=Accident.AID_LOST).count()

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='frecuency')
        value_detail.numerator = aids * 200000  # N°Accidentes con tiempo perdido x 200 000
        value_detail.denominator = hours_worked_in_month  # Horas Hombre Trabajadas Acumuladas

        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_icsst:
        denominator_icsst = Agreement.objects.filter(Q(company=company),
                                                     Q(date__month=month)).count()

        numerator_icsst = Agreement.objects.filter(Q(company=company), Q(percentage=100),
                                                   Q(date__month=month)).count()
        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='icsst')
        value_detail.numerator = numerator_icsst
        value_detail.denominator = denominator_icsst
        value_detail.save()
        if denominator_icsst == 0:
            index_detail.icsst = 0
        else:
            index_detail.icsst = numerator_icsst * 100.00 / denominator_icsst
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
                                                                     Q(date__month=month)).count()
        numerator_indice_no_conformidad = Agreement.objects.filter(Q(company=company), Q(percentage=100),
                                                                   Q(date__month=month)).count()

        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='indice_no_conformidad')

        value_detail.numerator = numerator_indice_no_conformidad
        value_detail.denominator = denominator_indice_no_conformidad
        value_detail.save()
        if denominator_indice_no_conformidad == 0:
            index_detail.indice_no_conformidad = 0
        else:
            index_detail.indice_no_conformidad = numerator_indice_no_conformidad * 100.00 / denominator_indice_no_conformidad
            # index_detail.save()
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
                                                            Q(date__month=month)).count()
        numerator_medida_iperc = Agreement.objects.filter(Q(company=company), Q(percentage=100.0),
                                                          Q(date__month=month)).count()
        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='medida_iperc')

        value_detail.numerator = numerator_medida_iperc
        value_detail.denominator = denominator_medida_iperc
        value_detail.save()
        if denominator_medida_iperc == 0:
            index_detail.medida_iperc = 0
        else:
            index_detail.medida_iperc = numerator_medida_iperc * 100.00 / denominator_medida_iperc
            # index_detail.save()
            # else:
            #     try:
            #         values = ValuesDetail.objects.get(detail=index_detail, key='medida_iperc')
            #     except:
            #         values = ValuesDetail(detail=index_detail, key='medida_iperc')
            #     numerator_medida_iperc = values.numerator
            #     denominator_medida_iperc = values.denominator
    if index.is_using_liderazgo:

        events = Events.objects.filter(event_start__month=month, calendar__company=company)
        for owner_index, owner_val in Events.OWNER:
            value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='lidership__' + owner_val)
            value_detail.numerator = events.filter(responsable=owner_index, state=DONE).count()
            value_detail.denominator = events.filter(responsable=owner_index).count()
            if value_detail.denominator > 0:
                value_detail.value = (value_detail.numerator * 100 / value_detail.denominator)
            else:
                value_detail.value = 0

            value_detail.save()



            # if index_detail.liderazgo == 0:
            # denominator_liderazgo = Agreement.objects.filter(Q(company=company),
            #                                                  Q(date__month=month)).count()
            # numerator_liderazgo = Agreement.objects.filter(Q(company=company), Q(percentage=100),
            #                                                Q(date__month=month)).count()
            # value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='liderazgo')
            #
            # value_detail.numerator = numerator_liderazgo
            # value_detail.denominator = denominator_liderazgo
            # value_detail.save()
            # if denominator_liderazgo == 0:
            #     index_detail.liderazgo = 0
            # else:
            #     index_detail.liderazgo = numerator_liderazgo * 100.00 / denominator_liderazgo
            # index_detail.save()
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
                                                                 Q(date__month=month)).count()
        numerator_plan_contingencia = Agreement.objects.filter(Q(company=company), Q(percentage=100),
                                                               Q(date__month=month)).count()
        # if not numerator_plan_contingencia:
        #     numerator_plan_contingencia = 0
        # try:
        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='plan_contingencia')
        # except:
        #     values = ValuesDetail(detail=index_detail, key='plan_contingencia')
        value_detail.numerator = numerator_plan_contingencia
        value_detail.denominator = denominator_plan_contingencia
        value_detail.save()
        if denominator_plan_contingencia == 0:
            index_detail.plan_contingencia = 0
        else:
            index_detail.plan_contingencia = numerator_plan_contingencia * 100.00 / denominator_plan_contingencia

    index_detail.save()

    if index.is_using_mejora:
        agreements = AgreementImprovement.objects.filter(date__month=month, company=company)
        value_detail, _ = ValuesDetail.objects.get_or_create(detail=index_detail, key='improvements')
        value_detail.numerator = agreements.filter(percentage=100).count()
        value_detail.denominator = agreements.count()
        if value_detail.denominator > 0:
            value_detail.value = value_detail.numerator * 100 / value_detail.denominator
        else:
            value_detail.value = 0
        value_detail.save()

    if index.is_using_severity:
        value_detail, _is_new = ValuesDetail.objects.get_or_create(detail=index_detail, key='severity')

    if index.is_using_accidentality:
        value_detail, _is_new = ValuesDetail.objects.get_or_create(detail=index_detail, key='accidentability')

    if index.is_using_professional_sick:
        value_detail, _is_new = ValuesDetail.objects.get_or_create(detail=index_detail, key='proffesional_sick')

    if index.is_using_medic_exam :
        value_detail, _is_new = ValuesDetail.objects.get_or_create(detail=index_detail, key='medic_exam')

    if index.is_using_ap_worker:
        value_detail, _is_new = ValuesDetail.objects.get_or_create(detail=index_detail, key='workers_up')

    if index.is_using_ap_worker_restric:
        value_detail, _is_new = ValuesDetail.objects.get_or_create(detail=index_detail, key='workers_up_restrictions')

    if index.is_using_medidas_control:
        value_detail, _is_new = ValuesDetail.objects.get_or_create(detail=index_detail, key='expose_quimic')

    if index.is_using_medidas_control:
        value_detail, _is_new = ValuesDetail.objects.get_or_create(detail=index_detail, key='occupational_monitor')

    if index.is_using_medidas_control:
        value_detail, _is_new = ValuesDetail.objects.get_or_create(detail=index_detail, key='measure_occupational_control')

    # else:
    #     try:
    #         values = ValuesDetail.objects.get(detail=index_detail, key='plan_contingencia')
    #     except:
    #         values = ValuesDetail(detail=index_detail, key='plan_contingencia')
    #     numerator_plan_contingencia = values.numerator
    #     denominator_plan_contingencia = values.denominator
    title = 'REPORTE MENSUAL SEGURIDAD Y SALUD OCUPACIONAL'
    date_now = datetime.now()
    return redirect(reverse('main:report_monthly', kwargs={'company_slug': company_slug, 'month': month}))


def monthly_report(request, company_slug, month):
    current_date = datetime.now()
    month_label = current_date.replace(day=1).replace(month=int(month)).strftime('%B')

    company = get_object_or_404(Company, slug=company_slug)
    counter = CountWorker.objects.get(month_year__month=month)
    workers_in_month = counter.workers

    if workers_in_month > 100:
        indice_general = 1000000
    else:
        indice_general = 200000

    index, _ = Index.objects.get_or_create(company=company)
    index_detail, _ = Index_Detail.objects.get_or_create(index=index, mounth=month)
    values_details = ValuesDetail.objects.filter(detail=index_detail)

    return render(request, 'main/reports/reports_mensual.html', locals())


@login_required
def reports(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    # months = []
    current_date = datetime.now()
    months = [{'mes': '{}'.format(_(current_date.replace(day=1).replace(month=i).strftime('%B'))), 'index': i} for i in
              range(1, 13)]
    year = datetime.now().year
    return render(request, "main/reports/reports.html", locals())
