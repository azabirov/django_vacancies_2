"""stepik_vacancies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job_app.views import (
                           main_view,
                           vacancies_view,
                           specialty_vacancies_view,
                           company_view, vacancy_view,
                           custom_handler404,
                           custom_handler500,
                           )
"""
– Главная  /
– Все вакансии списком   /vacancies
– Вакансии по специализации /vacancies/cat/frontend
– Карточка компании  /companies/345
– Одна вакансия /vacancies/22
"""

handler404 = custom_handler404
handler500 = custom_handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name="main"),
    path('vacancies/', vacancies_view, name="vacancies"),
    path('vacancies/cat/<str:specialty>/', specialty_vacancies_view, name="specialty_vacancies"),
    path('companies/<int:company>/', company_view, name="company"),
    path('vacancies/<int:vacancy>/', vacancy_view, name="vacancy"),
]
