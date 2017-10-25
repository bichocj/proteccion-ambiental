# -*- coding: utf-8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect

from main.forms import CountWorkerForm
from main.models import Company, CountWorker
from django.utils.translation import ugettext as _


def personal_counter_list(request, company_slug):
    company = get_object_or_404(Company, slug=company_slug)
    current_date = datetime.now()
    count_workers = CountWorker.objects.filter(month_year__year=current_date.year, company=company).order_by(
        'month_year')
    if count_workers.count() == 0:
        for i in range(1, 13):
            CountWorker(month_year=current_date.replace(month=i), quantity=0, company=company).save()
        count_workers = CountWorker.objects.filter(month_year__year=current_date.year, company=company).order_by(
            'month_year')

    return render(request, 'main/personal/counter/list.html', locals())


def personal_counter_edit(request, company_slug, counter_pk):
    company = get_object_or_404(Company, slug=company_slug)
    count_worker = get_object_or_404(CountWorker, pk=counter_pk)
    title = 'Editar Cantidad de Trabajadores para el mes de {}, {}'.format(
        _(count_worker.month_year.strftime('%B')),
        count_worker.month_year.strftime('%Y')
    )
    if request.POST:
        form = CountWorkerForm(request.POST, instance=count_worker)
        if form.is_valid():
            form.save()
        return redirect(reverse('main:personal_counter_list', kwargs={"company_slug": company_slug}))
    else:
        form = CountWorkerForm(instance=count_worker)

    return render(request, 'main/layout_form.html', locals())
