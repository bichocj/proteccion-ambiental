from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

from acuerdos_sst.forms import AgreementForm, AgreementDetailForm
from acuerdos_sst.models import Agreement, AgreementDetail
from main.models import Company


def home(request, company_slug):
    company = Company.objects.get(slug=company_slug)
    return render(request, 'acuerdos_sst/home.html', locals())


def agreement_new(request, company_slug):
    company = Company.objects.get(slug=company_slug)
    agreements = Agreement.objects.filter(company=company)
    if request.POST:
        form = AgreementForm(request.POST)
        if form.is_valid():
            agreement = form.save(commit=False)
            agreement.company = company
            agreement.save()
            return redirect(reverse('acuerdos_sst:agreement_detail',
                                    kwargs={"agreement_pk": agreement.pk, "company_slug": company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = AgreementForm()
    return render(request, 'acuerdos_sst/agreement.html', locals())


def agreement_list(request, company_slug):
    company = Company.objects.get(slug=company_slug)
    agreements = Agreement.objects.filter(company=company)
    return render(request, 'acuerdos_sst/list.html', locals())


def agreement_delete(request, agreement_pk, company_slug):
    company = Company.objects.get(slug=company_slug)
    agreement = Agreement.objects.get(pk=agreement_pk)
    agreement_details = AgreementDetail.objects.filter(Q(agreement=agreement),
                                                       (
                                                           Q(state=AgreementDetail.TO_DO) | Q(
                                                               state=AgreementDetail.DOING)))
    if agreement_details.count() > 0:
        message = 'No puede ser eliminado tiene tareas sin terminar'
        agreements = Agreement.objects.filter(company=company)
        return render(request, 'acuerdos_sst/list.html', locals())
    else:
        agreementsDetails = AgreementDetail.objects.filter(agreement=agreement)
        for ad in agreementsDetails:
            ad.delete()
        agreement.delete()
    return redirect(reverse('acuerdos_sst:agreement_list', kwargs={'company_slug': company_slug}))


def agreement_detail_delete(request, agreement_pk, company_slug, agreement_detail_pk):
    agreementdetail = AgreementDetail.objects.get(pk=agreement_detail_pk)
    agreementdetail.delete()
    return redirect(reverse('acuerdos_sst:agreement_detail',
                            kwargs={"agreement_pk": agreement_pk, "company_slug": company_slug}))


def agreement_detail_edit(request, agreement_pk, company_slug, agreement_detail_pk):
    title = 'Editar Detalle en acuerdo'
    agreement = Agreement.objects.get(pk=agreement_pk)
    agreements_details = AgreementDetail.objects.filter(agreement=agreement)
    agreementdetail = AgreementDetail.objects.get(pk=agreement_detail_pk)
    company = Company.objects.get(slug=company_slug)
    if request.POST:
        form = AgreementDetailForm(request.POST, request.FILES, instance=agreementdetail)
        if form.is_valid():
            form.save()
            return redirect(reverse('acuerdos_sst:agreement_detail',
                                    kwargs={"agreement_pk": agreement.pk, "company_slug": company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = AgreementDetailForm(instance=agreementdetail)
    return render(request, 'acuerdos_sst/details_agreement.html', locals())


def agreement_detail(request, agreement_pk, company_slug):
    title = 'Nuevo Detalle en acuerdo'
    agreement = Agreement.objects.get(pk=agreement_pk)
    company = Company.objects.get(slug=company_slug)
    if request.POST:
        form = AgreementDetailForm(request.POST, request.FILES)
        if form.is_valid():
            agd = form.save(commit=False)
            agd.agreement = agreement
            agd.save()
            return redirect(reverse('acuerdos_sst:agreement_detail',
                                    kwargs={"agreement_pk": agreement.pk, "company_slug": company_slug}))
        else:
            message = 'Revisa que la informacion sea correcta'
    else:

        form = AgreementDetailForm()
    agreements_details = AgreementDetail.objects.filter(agreement=agreement)
    return render(request, 'acuerdos_sst/details_agreement.html', locals())
