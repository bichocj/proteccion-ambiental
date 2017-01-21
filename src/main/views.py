from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .models import Company, Format, Requirement
from .forms import CompanyForm, FormatForm
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'main/home.html')


# panel de oshas
@login_required
def panel(request, pk):
    company = Company.objects.get(pk=pk)
    return render(request, 'main/panel.html', locals())


# panel de ley de seguridad ambiental
@login_required
def law(request):
    # if user is admin
    companies = Company.objects.all()
    # else
    # companies = Company.objects.get(su empresa)
    return render(request, "main/ley_seguridad.html", locals())


@login_required
def requirements_list(request, pk):
    company = Company.objects.get(pk=pk)
    requirements = Requirement.objects.filter(is_active=True).order_by('order')
    for requirement in requirements:
        requirement.formats = Format.objects.filter(requirement__pk=requirement.pk, company__pk=request.user.company.pk)
        for format in requirement.formats:
            format.form = FormatForm(instance=format)
    return render(request, "main/requirements/list.html", locals())


@login_required
def calendar(request, pk):
    company = Company.objects.get(pk=pk)
    return render(request, "main/calendar.html", locals())


@login_required
def new_company(request):
    title = "Nueva empresa"
    if request.POST:
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('main:law'))
    else:
        form = CompanyForm()
    return render(request, "main/hook/form.html", locals())


@login_required
def accidents(request, pk):
    company = Company.objects.get(pk=pk)
    return render(request, "main/accidents.html", locals())


@login_required
def agreement(request):
    return render(request, "main/agreement.html", locals())


@login_required
def reports(request, pk):
    company = Company.objects.get(pk=pk)
    return render(request, "main/reports.html", locals())

# @login_required
# def upload_file(request, pk):
#    newdoc = Format(document = request.FILES['document'])
#    newdoc.save(form)
#    return redirect("home")
#    form = UploadForm()
#        return render(request, 'index.html', locals())
