import datetime
import json

from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _

from fullcalendar.forms import CalendarModelForm, EventsModelForm
from fullcalendar.models import Calendar, Events, DOCTOR, DONE, INSPECTION, CAPACITATION, SIMULATION, CHARLAS, OTRO, \
    INDUCCION, CAPACITACION_DE_LEY, CAPACITACION_ESPECIFICA, CAPACITACION_SEGURIDAD, CAPACITACION_DE_SALUD_OCUPACIONAL, \
    ENTRENAMIENTO
from main.models import Company


def calendar_list(request, company_slug):
    group = Group.objects.get(name="Doctor")
    company = get_object_or_404(Company, slug=company_slug)

    if group in request.user.groups.all():
        calendars = Calendar.objects.filter(Q(company=company), Q(type=DOCTOR))
    else:
        calendars = Calendar.objects.filter(Q(company=company), ~Q(type=DOCTOR))
    return render(request, "fullcalendar/list.html", locals())


@login_required
def calendar_new(request, company_slug):
    title = _('Nuevo Cronograma')
    company = get_object_or_404(Company, slug=company_slug)
    calendar = True
    if request.POST:
        form = CalendarModelForm(request.POST, user=request.user)
        if form.is_valid():
            calendar = form.save(commit=False)
            group = Group.objects.get(name="Doctor")
            if group in request.user.groups.all():
                calendar.type = DOCTOR
            calendar.created_by = request.user
            calendar.company = company
            calendar.save()
            form.save_m2m()
            return redirect(reverse('fullcalendar:view_calendar', args=[company_slug, calendar.slug, calendar.id]))
        else:
            message = 'Revisa la informacion'
    else:
        form = CalendarModelForm(user=request.user)

    return render(request, "main/layout_form.html", locals())


@login_required
def calendar_edit(request, company_slug, calendar_id):
    title = _('Editar Cronorama')
    group = Group.objects.get(name="Doctor")
    company = get_object_or_404(Company, slug=company_slug)
    calendar = Calendar.objects.get(pk=calendar_id)
    if request.POST:
        form = CalendarModelForm(request.POST, instance=calendar, user=request.user)
        if form.is_valid():
            calendar = form.save(commit=False)
            if group in request.user.groups.all():
                calendar.type = DOCTOR
            calendar.save()
            return redirect(reverse('fullcalendar:calendar_list', args=[company_slug]))
        else:
            message = 'Revisa la informacion'
    else:
        if group in request.user.groups.all():
            calendar.type = None
        form = CalendarModelForm(instance=calendar, user=request.user)

    return render(request, "main/layout_form.html", locals())


@login_required
def calendar_delete(request, company_slug, calendar_id):
    company = get_object_or_404(Company, slug=company_slug)
    calendar = Calendar.objects.get(pk=calendar_id)
    events = Events.objects.filter(calendar=calendar)
    for e in events:
        e.delete()
    calendar.delete()
    return redirect(reverse('fullcalendar:calendar_list', args=[company_slug]))


@login_required
def view_calendar(request, company_slug, slug, calendar_id):
    calendar = True
    company = None
    try:
        company = get_object_or_404(Company, slug=company_slug)
        print('sluug', slug)
        calendar = Calendar.objects.get(company=company, slug=slug, id=calendar_id)
    except ObjectDoesNotExist:
        calendar = get_object_or_404(Calendar, id=calendar_id)
    dones = Events.objects.filter(state=DONE, calendar=calendar).count()
    not_do = Events.objects.filter(calendar=calendar).count() - dones
    # company = request.user.company
    form = EventsModelForm(calendar=calendar)
    info = {
        'view_calendar': {
            'name': calendar.title,
            'params': [slug, calendar.id]
        }
    }

    # breadcrumb = generate_breadcrumb_relations(links, 'view_calendar', info)
    return render(request, "fullcalendar/calendar.html", locals())


def events_json(request, calendar_id):
    calendar = get_object_or_404(Calendar, id=calendar_id)
    events_l = Events.objects.filter(calendar=calendar)
    events_list = []
    for event in events_l:
        event_start = event.event_start
        event_end = event.event_end

        all_day = event_start.hour == 0 and event_end.minute == 0

        if not event.is_cancelled:
            color = None
            if event.type_capacitations == INDUCCION:
                color = 'yellow'
            if event.type_capacitations == CAPACITACION_DE_LEY:
                color = 'red'
            if event.type_capacitations == CAPACITACION_ESPECIFICA:
                color = 'purple'
            if event.type_capacitations == CAPACITACION_SEGURIDAD:
                color = 'orange'
            if event.type_capacitations == CAPACITACION_DE_SALUD_OCUPACIONAL:
                color = 'red'
            if event.type_capacitations == ENTRENAMIENTO:
                color = 'blue'

            events_list.append({
                'id': event.id,
                'start': event_start.strftime('%Y-%m-%dT%H:%M%z'),
                'end': event_end.strftime('%Y-%m-%dT%H:%M%z'),
                'title': event.title,
                'allDay': all_day,
                "color": color
            })
    # if len(events_list) == 0:
    #    raise http.Http404
    # else:
    return http.HttpResponse(json.dumps(events_list), content_type="application/json")


def save_event(request, slug):
    response = {}
    if request.POST:
        print(request.FILES)
        if request.POST.get('id'):
            e = get_object_or_404(Events, pk=request.POST.get('id'))
            form = EventsModelForm(request.POST, request.FILES, instance=e)
        else:
            form = EventsModelForm(request.POST, request.FILES)
        print('gogogo')
        if form.is_valid():
            print('gogogox2')
            calendar = get_object_or_404(Calendar, slug=slug)
            event = form.save(commit=False)
            event.calendar = calendar
            event.created_by = request.user
            if event.calendar.type == CAPACITATION:
                event.type_inspeccions = None
            if event.calendar.type == INSPECTION:
                event.type_capacitations = None
                event.hours_worked = float(0)
                event.number_workers = 0
            if event.calendar.type == OTRO or event.calendar.type == SIMULATION or event.calendar.type == DOCTOR:
                event.type_inspeccions = None
                event.type_capacitations = None
                event.hours_worked = float(0)
                event.number_workers = 0

            if event.calendar.type == CHARLAS:
                event.type_inspeccions = None
                event.type_capacitations = None

            event.type = event.calendar.type

            event.save()

            color = None
            if event.type_capacitations == INDUCCION:
                color = 'yellow'
            if event.type_capacitations == CAPACITACION_DE_LEY:
                color = 'red'
            if event.type_capacitations == CAPACITACION_ESPECIFICA:
                color = 'purple'
            if event.type_capacitations == CAPACITACION_SEGURIDAD:
                color = 'orange'
            if event.type_capacitations == CAPACITACION_DE_SALUD_OCUPACIONAL:
                color = 'red'
            if event.type_capacitations == ENTRENAMIENTO:
                color = 'blue'

            response['success'] = True
            response['message'] = _("Save Success")
            response['id'] = event.id
            response['title'] = event.title
            response['start'] = event.event_start.strftime('%Y-%m-%d %I:%M %p %z')
            response['end'] = event.event_end.strftime('%Y-%m-%d %I:%M %p %z')
            response['allDay'] = event.event_start.hour == 0 and event.event_end.minute == 0
            response['color'] = color
        else:
            response['success'] = False
            print(form.errors)
            errors = form.errors
            response['errors'] = list(errors)
    else:
        response['success'] = True
        response['message'] = _("Invalid request")
    return http.HttpResponse(
        json.dumps(response),
        content_type="application/json"
    )


def get_event(request):
    response = {}
    import os
    if request.POST:
        event_id = request.POST.get('id')
        event = get_object_or_404(Events, id=event_id)
        response['success'] = True
        response['data'] = {
            'event': event.id,
            'event_start': event.event_start.strftime('%Y-%m-%d %I:%M %p %z'),
            'event_end': event.event_end.strftime('%Y-%m-%d %I:%M %p %z'),
            'title': event.title,
            'description': event.description,
            'observation': event.observation,
            'state': event.state,
            'type': event.type,
            'hours_worked': event.hours_worked,
            'number_workers': event.number_workers,
            'responsable': event.responsable,
            'type_capacitations': event.type_capacitations,
            'evidence_name': os.path.basename(event.evidence.name) if event.evidence else 'Ninguno',
            'url_evidence': event.evidence.url if event.evidence else 'Ninguno',

            # 'member': event.member.id,
            # 'member_fullname': event.member.first_name + ' ' + event.member.last_name
        }

        # 'type_inspeccion': event.type_inspeccion
    else:
        response['success'] = False
        response['message'] = _("Invalid request")
    return http.HttpResponse(json.dumps(response), content_type="application/json")


def update_event(request, slug):
    response = {}
    if request.POST:
        print(request.FILES)
        if request.POST.get('id'):
            e = get_object_or_404(Events, pk=request.POST.get('id'))
            form = EventsModelForm(request.POST, request.FILES, instance=e)
        else:
            form = EventsModelForm(request.POST, request.FILES)
        print('gogogo')
        if form.is_valid():
            print('gogogox2')
            calendar = get_object_or_404(Calendar, slug=slug)
            event = form.save(commit=False)
            event.calendar = calendar
            event.created_by = request.user
            if event.calendar.type == CAPACITATION:
                event.type_inspeccions = None
            if event.calendar.type == INSPECTION:
                event.type_capacitations = None
                event.hours_worked = 0
                event.number_workers = 0
            if event.calendar.type == OTRO or event.calendar.type == SIMULATION or event.calendar.type == DOCTOR:
                event.type_inspeccions = None
                event.type_capacitations = None
                event.number_workers = float(0)
                event.hours_worked = 0

            if event.calendar.type == CHARLAS:
                event.type_inspeccions = None
                event.type_capacitations = None

            event.type = event.calendar.type

            if event.evidence:
                event.state = DONE

            color = None
            if event.type_capacitations == INDUCCION:
                color = 'yellow'
            if event.type_capacitations == CAPACITACION_DE_LEY:
                color = 'red'
            if event.type_capacitations == CAPACITACION_ESPECIFICA:
                color = 'purple'
            if event.type_capacitations == CAPACITACION_SEGURIDAD:
                color = 'orange'
            if event.type_capacitations == CAPACITACION_DE_SALUD_OCUPACIONAL:
                color = 'red'
            if event.type_capacitations == ENTRENAMIENTO:
                color = 'blue'

            event.save()
            response['success'] = True
            response['message'] = _("Save Success")
            response['id'] = event.id
            response['title'] = event.title
            response['start'] = event.event_start.strftime('%Y-%m-%d %I:%M %p %z')
            response['end'] = event.event_end.strftime('%Y-%m-%d %I:%M %p %z')
            response['allDay'] = event.event_start.hour == 0 and event.event_end.minute == 0
            response['color'] = color
        else:
            response['success'] = False
            print(form.errors)
            errors = form.errors
            response['errors'] = list(errors)
    else:
        response['success'] = True
        response['message'] = _("Invalid request")
    return http.HttpResponse(
        json.dumps(response),
        content_type="application/json")


def settings_calendar(request, slug):
    company = request.user.company
    instance = get_object_or_404(Calendar, slug=slug)

    info = {
        'settings_calendar': {
            'params': [slug]
        },
        'view_calendar': {
            'name': instance.title,
            'params': [slug, instance.id]
        }
    }

    # breadcrumb = generate_breadcrumb_relations(links, 'settings_calendar', info)
    if request.POST:
        form = CalendarModelForm(request.POST, instance=instance)
        if form.is_valid():
            calendar = form.save()
            return redirect(reverse('fullcalendar:view_calendar', args=[calendar.slug, calendar.id]))
    else:
        form = CalendarModelForm(instance=instance)
        width = 12
    return render(request, "main/base_form.html", locals())
