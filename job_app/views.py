from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, ListView

from job_app.forms import RegistrationForm, LoginForm, ApplicationForm, CompanyForm, VacancyForm, ResumeForm
from job_app.models import Vacancy, Specialty, Company, Application, Resume

"""
– Главная  /
– Все вакансии списком   /vacancies
– Вакансии по специализации /vacancies/cat/frontend
– Карточка компании  /companies/345
– Одна вакансия /vacancies/22
"""
"""
– Отправка заявки /vacancies/<vacancy_id>/send/
– Моя компания (предложение создать) /mycompany/letsstart/
– Моя компания (пустая форма) /mycompany/create/
– Моя компания (заполненная форма) /mycompany/
– Мои вакансии (список) /mycompany/vacancies/
– Мои вакансии (пустая форма) /mycompany/vacancies/create/
– Одна моя вакансия (заполненная форма)  /mycompany/vacancies/<vacancy_id>

– Вход /login
– Регистрация /register
– Выход /logout
"""


class MainView(View):
    def get(self, request):
        specialties = Specialty.objects.annotate(count=Count('vacancies'))
        companies = Company.objects.annotate(num_vacancies=Count('vacancies'))
        return render(request, "week3/index.html", context={"specialties": specialties, "companies": companies})


class VacanciesView(View):
    def get(self, request):
        specialties = Specialty.objects.all()
        vacancies = Vacancy.objects.all()
        return render(request, "week3/vacancies.html", context={"specialties": specialties, "vacancies": vacancies})


class SpecialtyVacanciesView(View):
    def get(self, request, specialty_):
        try:
            specialties = Specialty.objects.filter(code=specialty_)
        except Specialty.DoesNotExist:
            raise Http404
        return render(request, "week3/vacancies.html", context={"specialties": specialties})


class CompanyView(View):
    def get(self, request, company):
        try:
            company = Company.objects.get(id=company)
        except Company.DoesNotExist:
            raise Http404
        return render(request, "week3/company.html", context={"company": company})


class VacancyView(View):
    def get(self, request, vacancy):
        try:
            vacancy = Vacancy.objects.get(id=vacancy)
        except Vacancy.DoesNotExist:
            raise Http404
        return render(request, "week3/vacancy.html", context={"vacancy": vacancy, "form": ApplicationForm})

    def post(self, request, vacancy):
        application_form = ApplicationForm(request.POST)
        if application_form.is_valid():
            written_username = application_form.cleaned_data.get('written_username')
            written_phone = application_form.cleaned_data.get('written_phone')
            written_cover_letter = application_form.cleaned_data.get('written_cover_letter')
            user = request.user.id
            if user:
                Application.objects.create(
                                           written_username=written_username,
                                           written_phone=written_phone,
                                           written_cover_letter=written_cover_letter,
                                           user_id=user,
                                           vacancy=Vacancy.objects.get(id=vacancy),
                                           )
            else:
                return redirect('login')
            return redirect('sent', vacancy)
        return render(request, "week3/vacancy.html", context={"form": ApplicationForm})


class VacancySendView(View):
    def get(self, request, vacancy):
        return render(request, "week4/sent.html", context={"vacancy": vacancy})


class CompanyLetsStart(View):
    def get(self, request):
        user = auth.get_user(request)
        if Company.objects.filter(owner_id=user.id):
            return redirect('mycompanyedit')
        return render(request, "week3/company-create.html")


class MyCompanyView(View):
    def get(self, request):
        user = auth.get_user(request)
        if Company.objects.filter(owner_id=user.id):
            company = Company.objects.get(owner_id=user.id).id
            return redirect('company', company)
        return redirect('letsstart')


class MyCompanyEdit(View):
    success_message = "Информация о компании обновлена"

    def get(self, request):
        user = auth.get_user(request)
        company = None
        companyform = CompanyForm()
        if Company.objects.filter(owner_id=user.id):
            company = Company.objects.get(owner_id=user.id)
            companyform = CompanyForm(instance=company)
        return render(request, 'week3/company-edit.html', context={'form': companyform, 'company': company})


    def post(self, request):
        user = auth.get_user(request)
        messages.success(self.request, self.success_message)
        if Company.objects.filter(owner_id=user.id):
            company = Company.objects.get(owner_id=user.id)
            company_form = CompanyForm(request.POST, request.FILES, instance=company)
            company_form.instance.logo = company.logo
        else:
            company = None
            company_form = CompanyForm(request.POST, request.FILES)
        if company_form.is_valid():
            company_form.save(commit=False)
            company_form.instance.owner = request.user
            company_form.save()
            return redirect('mycompanyedit')
        return render(request, 'week3/company-edit.html', context={'form': company_form, 'company': company})


class MyCompanyCreate(View):
    def get(self, request):
        user = auth.get_user(request)
        company = None
        companyform = CompanyForm()
        if Company.objects.filter(owner_id=user.id):
            raise Http404
        else:
            return render(request, 'week3/company-edit.html', context={'form': companyform, 'company': company})


class MyVacancyEditView(View):
    success_message = "Вакансия обновлена"

    def get(self, request):
        vacancy_form = VacancyForm()
        return render(request, 'week4/vacancy-edit.html', context={'form': vacancy_form})

    def post(self, request):
        messages.success(self.request, self.success_message)
        vacancy_form = VacancyForm(request.POST)
        company = Company.objects.filter(owner_id=request.user.id).first()
        if vacancy_form.is_valid():
            vacancy_form.instance.company = company
            vacancy_form.save()
            return render(request, 'week4/vacancy-edit.html', context={'form': vacancy_form})


class MyVacancy(View):
    def get(self, request, vacancy):
        user = auth.get_user(request)
        if Vacancy.objects.filter(company__owner__id=user.id).filter(id=vacancy).exists():
            return redirect('vacancy', vacancy)
        else:
            raise Http404


class MyVacanciesView(View):
    def get(self, request):
        user = auth.get_user(request)
        jobs = Vacancy.objects.filter(company__owner__id=user.id).annotate(application_count=Count('applications'))
        if not jobs:
            return redirect('myvacanciescreate')
        return render(request, 'week4/vacancy-list.html', context={'vacancies': jobs})


class MyVacanciesCreateView(View):
    def get(self, request):
        user = auth.get_user(request)
        vacancies = Vacancy.objects.filter(company__owner__id=user.id).annotate(application_count=Count('applications'))
        if vacancies:
            return redirect('myvacancyedit')
        return render(request, 'week4/vacancy-create.html')


class MyResumeLetsStart(View):
    def get(self, request):
        user = auth.get_user(request)
        if Resume.objects.filter(owner_id=user.id):
            return redirect('myresume')
        return render(request, "week4/resume-create.html")


class MyResumeEditView(View):
    success_message = "Резюме обновлено"

    def get(self, request):
        user = auth.get_user(request)
        resume = None
        resumeform = ResumeForm()
        if Resume.objects.filter(owner_id=user.id):
            resume = Resume.objects.get(owner_id=user.id)
            resumeform = ResumeForm(instance=resume)
        return render(request, 'week4/resume-edit.html', context={'form': resumeform, 'resume': resume})

    def post(self, request):
        user = auth.get_user(request)
        messages.success(self.request, self.success_message)
        if Resume.objects.filter(owner_id=user.id):
            resume = Resume.objects.get(owner_id=user.id)
            resume_form = ResumeForm(request.POST, instance=resume)
        else:
            resume = None
            resume_form = ResumeForm(request.POST)
        if resume_form.is_valid():
            resume_form.save(commit=False)
            resume_form.instance.owner = request.user
            resume_form.save()
            return redirect('myresumeedit')
        return render(request, 'week4/resume-edit.html', context={'form': resume_form, 'resume': resume})


class MyResumeCreateView(View):
    def get(self, request):
        user = auth.get_user(request)
        if Resume.objects.filter(owner_id=user.id):
            raise Http404
        else:
            return redirect('myresumeedit')


class RegisterView(CreateView):
    form_class = RegistrationForm
    model = User
    success_url = "login"
    template_name = "week4/register.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('/login/')


class SearchView(ListView):
    model = Vacancy
    template_name = "week4/search.html"

    def get_queryset(self):
        request = self.request.GET.get('s')
        return Vacancy.objects.filter(
            Q(title__icontains=request) | Q(description__icontains=request) | Q(skills__icontains=request)
        )


class LogoutView(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect("main")


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect("main")
    return render(request, 'week4/login.html', {'form': form})


def custom_handler500(request, *args, **kwargs):
    return HttpResponse(
        "<h2>500 ERROR - Server error.</h2><p>We wish you at least some level of "
        "patience.</p>",
        status=500,
    )


def custom_handler404(request, *args, **kwargs):
    return render(request, '404.html')
