from django.shortcuts import render
from django.http import HttpResponse
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
    return render(request, "week3/index.html", context={})


def vacancies_view(request):
    return render(request, "week3/vacancies.html", context={})


def specialty_vacancies_view(request, specialty):
    return render(request, "week3/vacancies.html", context={})


def company_view(request, company):
    return render(request, "week3/company.html", context={})


def vacancy_view(request, vacancy):
    return render(request, "week3/vacancy.html", context={})


def custom_handler500(request, *args, **kwargs):
    return HttpResponse("500 ERROR - Server error.", status=500)


def custom_handler404(request, *args, **kwargs):
    return HttpResponse("404 ERROR - No such page.", status=404)