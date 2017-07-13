import datetime
import json

from django import http
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import ugettext as _

from fullcalendar.forms import CalendarModelForm, EventsModelForm
from fullcalendar.models import Calendar, Events
from main.models import Company


def calendar_list(request, company_slug):
    calendars = Calendar.objects.all()
    company = get_object_or_404(Company, slug=company_slug)
    return render(request, "fullcalendar/list.html", locals())


@login_required
def calendar_new(request, company_slug):
    title = _('Nuevo Cronograma')
    company = get_object_or_404(Company, slug=company_slug)
    calendar = True
    if request.POST:
        form = CalendarModelForm(request.POST)
        if form.is_valid():
            calendar = form.save(commit=False)
            calendar.created_by = request.user
            calendar.company = company
            calendar.save()
            form.save_m2m()
            return redirect(reverse('fullcalendar:view_calendar', args=[company_slug, calendar.slug, calendar.id]))
        else:
            message = 'Revisa la informacion'
    else:
        form = CalendarModelForm()

    return render(request, "main/layout_form.html", locals())


@login_required
def calendar_edit(request, company_slug, calendar_id):
    title = _('Editar Cronorama')
    company = get_object_or_404(Company, slug=company_slug)
    calendar = Calendar.objects.get(pk=calendar_id)
    if request.POST:
        form = CalendarModelForm(request.POST, instance=calendar)
        if form.is_valid():
            calendar.save()
            return redirect(reverse('fullcalendar:calendar_list', args=[company_slug]))
        else:
            message = 'Revisa la informacion'
    else:
        form = CalendarModelForm(instance=calendar)

    return render(request, "main/layout_form.html", locals())


@login_required
def calendar_delete(request, company_slug, calendar_id):
    company = get_object_or_404(Company, slug=company_slug)
    calendar = Calendar.objects.get(pk=calendar_id)
    calendar.delete()
    return redirect(reverse('fullcalendar:calendar_list', args=[company_slug]))


@login_required
def view_calendar(request, company_slug, slug, calendar_id):
    calendar = True
    try:
        company = get_object_or_404(Company, slug=company_slug)
        print('sluug', slug)
        calendar = Calendar.objects.get(company=company, slug=slug, id=calendar_id)
    except ObjectDoesNotExist:
        calendar = get_object_or_404(Calendar, id=calendar_id)
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
            events_list.append({
                'id': event.id,
                'start': event_start.strftime('%Y-%m-%d %H:%M'),
                'end': event_end.strftime('%Y-%m-%d %H:%M'),
                'title': event.title,
                'allDay': all_day
            })
    # if len(events_list) == 0:
    #    raise http.Http404
    # else:
    return http.HttpResponse(json.dumps(events_list), content_type="application/json")


def save_event(request, slug):
    response = {}
    if request.POST:
        if request.POST.get('id'):
            e = get_object_or_404(Events, pk=request.POST.get('id'))
            form = EventsModelForm(request.POST, instance=e)
        else:
            form = EventsModelForm(request.POST)
        print('gogogo')
        if form.is_valid():
            print('gogogox2')
            calendar = get_object_or_404(Calendar, slug=slug)
            event = form.save(commit=False)
            event.calendar = calendar
            event.created_by = request.user
            if event.calendar.type == Calendar.CAPACITATION:
                event.type_inspeccions = None
            if event.calendar.type == Calendar.INSPECTION:
                event.type_capacitations = None
                event.hours_worked = None
                event.number_workers = None
            if event.calendar.type == Calendar.OTRO or event.calendar.type == Calendar.CHARLAS or event.calendar.type == Calendar.SIMULATION:
                event.type_inspeccions = None
                event.type_capacitations = None
                event.number_workers = None
                event.hours_worked = None
            print(request.POST)
            print(event.type_inspeccions)
            event.type = event.calendar.type
            print(event.type)
            event.save()
            print('gogogox4')
            response['success'] = True
            response['message'] = _("Save Success")
            response['id'] = event.id
            response['title'] = event.title
            response['start'] = event.event_start.strftime('%Y-%m-%d %I:%M %p %z')
            response['end'] = event.event_end.strftime('%Y-%m-%d %I:%M %p %z')
            response['allDay'] = event.event_start.hour == 0 and event.event_end.minute == 0
        else:
            response['success'] = False
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
            'responsable': event.responsable.name,
            'type_capacitations': event.type_capacitations,

            # 'member': event.member.id,
            # 'member_fullname': event.member.first_name + ' ' + event.member.last_name
        }

        # 'type_inspeccion': event.type_inspeccion
    else:
        response['success'] = False
        response['message'] = _("Invalid request")
    return http.HttpResponse(json.dumps(response), content_type="application/json")


def update_event(request):
    response = {}
    if request.POST:
        event_id = request.POST.get('id')
        event = get_object_or_404(Events, id=event_id)

        event.event_start = datetime.datetime.strptime(request.POST.get('start'), '%d/%m/%Y %I:%M %p')
        event.event_end = datetime.datetime.strptime(request.POST.get('end'), '%d/%m/%Y %I:%M %p')
        event.title = request.POST.get('title')
        event.save()

        response['success'] = True
        response['data'] = {
            'event': event.id,
            'event_start': event.event_start.strftime('%Y-%m-%d %I:%M %p %z'),
            'event_end': event.event_end.strftime('%Y-%m-%d %I:%M %p %z'),
            'title': event.title,
            'description': event.description,
            'observation': event.observation,
            'hours_worked': event.hours_worked,
            'number_workers': event.number_workers
            # 'member': event.member.id
        }
    else:
        response['success'] = False
        response['message'] = _("Invalid request")
    return http.HttpResponse(json.dumps(response), content_type="application/json")


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
