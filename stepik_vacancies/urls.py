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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from job_app.views import (
                           MainView,
                           login_view,
                           LogoutView,
                           RegisterView,
                           VacanciesView,
                           SpecialtyVacanciesView,
                           CompanyView, VacancyView,
                           VacancySendView,
                           CompanyLetsStart,
                           MyCompanyView,
                           MyCompanyCreate,
                           MyCompanyEdit,
                           MyVacanciesView,
                           MyVacanciesCreateView,
                           MyVacancyEditView,
                           MyVacancy,
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
    path('', MainView.as_view(), name="main"),
    path('login/', login_view, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('vacancies/', VacanciesView.as_view(), name="vacancies"),
    path('vacancies/cat/<str:specialty_>/', SpecialtyVacanciesView.as_view(), name="specialty_vacancies"),
    path('companies/<int:company>/', CompanyView.as_view(), name="company"),
    path('vacancies/<int:vacancy>/', VacancyView.as_view(), name="vacancy"),
    path('vacancies/<int:vacancy>/send/', VacancySendView.as_view(), name="sent"),
    path('mycompany/letsstart/', login_required(CompanyLetsStart.as_view()), name="letsstart"),
    path('mycompany/', login_required(MyCompanyView.as_view()), name="mycompany"),
    path('mycompany/create/', login_required(MyCompanyCreate.as_view()), name='mycompanycreate'),
    path('mycompany/edit/', login_required(MyCompanyEdit.as_view()), name='mycompanyedit'),
    path('mycompany/vacancies/', login_required(MyVacanciesView.as_view()), name='myvacancies'),
    path('mycompany/vacancies/create/', login_required(MyVacanciesCreateView.as_view()), name='myvacanciescreate'),
    path('mycompany/vacancies/edit/', login_required(MyVacancyEditView.as_view()), name='myvacancyedit'),
    path('mycompany/vacancies/<int:vacancy>/', login_required(MyVacancy.as_view()), name='myvacancy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
