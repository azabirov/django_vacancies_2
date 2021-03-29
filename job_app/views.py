from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse, Http404
from job_app.models import Vacancy, Specialty, Company
# Create your views here.
"""
– Главная  /
– Все вакансии списком   /vacancies
– Вакансии по специализации /vacancies/cat/frontend
– Карточка компании  /companies/345
– Одна вакансия /vacancies/22
"""


def main_view(request):
    specialties = Specialty.objects.annotate(count=Count('vacancies'))
    companies = Company.objects.annotate(num_vacancies=Count('vacancies'))
    return render(request, "week3/index.html", context={"specialties": specialties, "companies": companies})


def vacancies_view(request):
    specialties = Specialty.objects.all()
    vacancies = Vacancy.objects.all()
    return render(request, "week3/vacancies.html", context={"specialties": specialties, "vacancies": vacancies})


def specialty_vacancies_view(request, specialty_):
    try:
        specialties = Specialty.objects.filter(code=specialty_)
    except Specialty.DoesNotExist:
        raise Http404
    return render(request, "week3/vacancies.html", context={"specialties": specialties})


def company_view(request, company):
    try:
        company = Company.objects.get(id=company)
    except Company.DoesNotExist:
        raise Http404
    return render(request, "week3/company.html", context={"company": company})


def vacancy_view(request, vacancy):
    try:
        vacancy = Vacancy.objects.get(id=vacancy)
    except Vacancy.DoesNotExist:
        raise Http404
    return render(request, "week3/vacancy.html", context={"vacancy": vacancy})


def custom_handler500(request, *args, **kwargs):
    return HttpResponse(
        "<h2>500 ERROR - Server error.</h2><p>We wish you at least some level of patience.</p>",
        status=500,
     )


def custom_handler404(request, *args, **kwargs):
    return HttpResponse(
        "<h2>404 ERROR - No such page.</h2><p>Oops! Sorry for that, but you have to type the right path.</p>",
        status=404,
    )
