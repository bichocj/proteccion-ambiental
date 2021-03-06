from decimal import Decimal

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render, redirect

from improvements.forms import AgreementForm, AgreementDetailForm, MettingForm
from improvements.models import Agreement, AgreementDetail, Metting
from main.models import Company


# Metting Block
def meeting_list(request, company_slug):
    company = Company.objects.get(slug=company_slug)
    meetings = Metting.objects.filter(company=company)
    return render(request, 'improvements/meetings/list.html', locals())


def meeting_new(request, company_slug):
    company = Company.objects.get(slug=company_slug)
    title = 'Nueva Reunion de Mejora'
    if request.POST:
        form = MettingForm(request.POST, request.FILES)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.company = company
            meeting.save()
            form.save_m2m()
            return redirect(reverse('improvements:agreement_list',
                                    kwargs={"meeting_pk": meeting.pk, "company_slug": company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = MettingForm()
    return render(request, 'main/layout_form.html', locals())


def meeting_edit(request, meeting_pk, company_slug):
    company = Company.objects.get(slug=company_slug)
    meeting = Metting.objects.get(pk=meeting_pk)
    title = 'Editar Reunion de Acuerdo de Comite SST'
    if request.POST:
        form = MettingForm(request.POST, instance=meeting)
        if form.is_valid():
            agreement = form.save(commit=False)
            agreement.company = company
            agreement.save()
            return redirect(reverse('improvements:agreement_list',
                                    kwargs={"meeting_pk": meeting_pk,
                                            "company_slug": company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = MettingForm(instance=meeting)
    return render(request, 'main/layout_form.html', locals())


def meeting_delete(request, meeting_pk, company_slug):
    company = Company.objects.get(slug=company_slug)
    meeting = Metting.objects.get(pk=meeting_pk)
    agreements = Agreement.objects.filter(metting=meeting)
    for agreement in agreements:
        if not agreement.percentage or agreement.percentage < 100.00:
            message = 'No puede ser eliminado tiene acuerdos sin terminar'
            meetings = Metting.objects.filter(company=company)
            return render(request, 'improvements/meetings/list.html', locals())
    for agreement in agreements:
        agreementsDetails = AgreementDetail.objects.filter(agreement=agreement)
        for ad in agreementsDetails:
            ad.delete()
        agreement.delete()
    meeting.delete()
    return redirect(
        reverse('improvements:meeting_list', kwargs={'company_slug': company_slug}))


# Agreement Block
def agreement_list(request, meeting_pk, company_slug):
    company = Company.objects.get(slug=company_slug)
    meeting = Metting.objects.get(pk=meeting_pk)
    agreements = Agreement.objects.filter(company=company, metting__id=meeting_pk, is_active=True)
    return render(request, 'improvements/list.html', locals())


def agreement_new(request, meeting_pk, company_slug):
    company = Company.objects.get(slug=company_slug)
    meeting = Metting.objects.get(pk=meeting_pk)
    title = 'Nuevo Acuerdo de Comite SST'
    agreements = Agreement.objects.filter(company=company)
    if request.POST:
        form = AgreementForm(request.POST)
        if form.is_valid():
            agreement = form.save(commit=False)
            agreement.company = company
            agreement.metting = meeting
            agreement.save()
            return redirect(reverse('improvements:agreement_detail',
                                    kwargs={"agreement_pk": agreement.pk, "company_slug": company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = AgreementForm()
    return render(request, 'main/layout_form.html', locals())


def agreement_edit(request, meeting_pk, agreement_pk, company_slug):
    company = Company.objects.get(slug=company_slug)
    meeting = Metting.objects.get(pk=meeting_pk)
    agreement = Agreement.objects.get(pk=agreement_pk)
    title = 'Editar Acuerdo de Comite SST'
    if request.POST:
        form = AgreementForm(request.POST, instance=agreement)
        if form.is_valid():
            agreement = form.save(commit=False)
            agreement.company = company
            agreement.metting = meeting
            agreement.save()
            return redirect(reverse('improvements:agreement_list',
                                    kwargs={"meeting_pk": meeting_pk,
                                            "company_slug": company_slug}
                                    ))
        else:
            message = 'Revisa la informacion'
    else:
        form = AgreementForm(instance=agreement)
    return render(request, 'main/layout_form.html', locals())


def agreement_delete(request, agreement_pk, meeting_pk, company_slug):
    company = Company.objects.get(slug=company_slug)
    meeting = Metting.objects.get(pk=meeting_pk)
    agreement = Agreement.objects.get(pk=agreement_pk)
    agreement_details = AgreementDetail.objects.filter(Q(agreement=agreement),
                                                       (
                                                           Q(state=AgreementDetail.TO_DO) | Q(
                                                               state=AgreementDetail.DOING)))
    if agreement_details.count() > 0:
        message = 'No puede ser eliminado tiene tareas sin terminar'
        agreements = Agreement.objects.filter(company=company, metting=meeting)
        return render(request, 'improvements/list.html', locals())
    else:
        agreementsDetails = AgreementDetail.objects.filter(agreement=agreement)
        for ad in agreementsDetails:
            ad.delete()
        agreement.delete()
    return redirect(
        reverse('improvements:agreement_list', kwargs={'company_slug': company_slug, 'meeting_pk': meeting_pk}))


def desactive_agreement(request, company_slug, agreement_pk):
    company = Company.objects.get(slug=company_slug)
    agreement = Agreement.objects.get(pk=agreement_pk)
    agreement.is_active = False
    agreement.save()
    return redirect(reverse('improvements:agreement_list', kwargs={'company_slug': company_slug}))


def cal_porcentage_progreess(agreement_pk):
    agreement = Agreement.objects.get(pk=agreement_pk)
    agreement_details = AgreementDetail.objects.filter(agreement=agreement)
    if agreement_details.count() <= 0:
        agreement.percentage = None
        agreement.save()
        return
    else:
        agreement_detail_with_DONE = AgreementDetail.objects.filter(Q(agreement=agreement),
                                                                    ~Q(state=AgreementDetail.DONE))
        if agreement_detail_with_DONE.count() <= 0:
            percentage = 100.0
        else:
            if agreement_detail_with_DONE.count() == agreement_details.count():
                percentage = 0.0
            else:
                percentage = (Decimal(agreement_detail_with_DONE.count()) * 100) / Decimal(agreement_details.count())
        agreement.percentage = percentage
        agreement.save()
        update_meeting(agreement.metting)


def update_meeting(metting):
    agreements = Agreement.objects.filter(Q(metting=metting), Q(percentage=Decimal(100.0)))
    agreements_all = Agreement.objects.filter(Q(metting=metting))
    metting.percentage = Decimal(Decimal(agreements.count()) * 100 / Decimal(agreements_all.count()))
    metting.save()


def agreement_detail_delete(request, agreement_pk, company_slug, agreement_detail_pk):
    agreementdetail = AgreementDetail.objects.get(pk=agreement_detail_pk)
    agreementdetail.delete()
    cal_porcentage_progreess(agreement_pk)
    return redirect(reverse('improvements:agreement_detail',
                            kwargs={"agreement_pk": agreement_pk, "company_slug": company_slug}))


def agreement_detail_new(request, agreement_pk, company_slug):
    company = Company.objects.get(slug=company_slug)
    agreement = Agreement.objects.get(pk=agreement_pk)
    title = 'Nueva <b>tarea</b> al acuerdo ' + agreement.title
    if request.POST:
        form = AgreementDetailForm(request.POST, request.FILES)
        if form.is_valid():
            agreement_detail = form.save(commit=False)
            agreement_detail.agreement = agreement
            agreement_detail.save()

            cal_porcentage_progreess(agreement_pk)
            return redirect(reverse('improvements:agreement_detail',
                                    kwargs={"agreement_pk": agreement.pk, "company_slug": company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = AgreementDetailForm()
    return render(request, 'main/layout_form.html', locals())


def agreement_detail_edit(request, agreement_pk, company_slug, agreement_detail_pk):
    title = 'Editar Detalle en acuerdo'
    agreement = Agreement.objects.get(pk=agreement_pk)
    meeting = agreement.metting
    agreements_details = AgreementDetail.objects.filter(agreement=agreement)
    agreement_detail = AgreementDetail.objects.get(pk=agreement_detail_pk)
    company = Company.objects.get(slug=company_slug)
    if request.POST:
        form = AgreementDetailForm(request.POST, request.FILES, instance=agreement_detail)
        if form.is_valid():
            form.save()
            cal_porcentage_progreess(agreement_pk)
            return redirect(reverse('improvements:agreement_detail',
                                    kwargs={"agreement_pk": agreement.pk, "company_slug": company_slug}))
        else:
            message = 'Revisa la informacion'
    else:
        form = AgreementDetailForm(instance=agreement_detail)
    return render(request, 'main/layout_form.html', locals())


def agreement_detail(request, agreement_pk, company_slug):
    title = 'Nuevo Detalle en acuerdo'
    agreement = Agreement.objects.get(pk=agreement_pk)
    meeting = agreement.metting
    company = Company.objects.get(slug=company_slug)
    agreements_details = AgreementDetail.objects.filter(agreement=agreement)
    return render(request, 'improvements/agreement/list.html', locals())
