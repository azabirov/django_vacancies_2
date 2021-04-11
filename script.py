"""
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'stepik_vacancies.settings'
django.setup()

from data import jobs, companies, specialties
from job_app.models import Vacancy, Company, Specialty

if __name__ == '__main__':
        for company in companies:
            state = Company.objects.create(
                name=company["title"],
                location=company["location"],
                logo=company["logo"],
                description=company["description"],
                employee_count=company["employee_count"],
            )
    
        for specialty in specialties:
            state = Specialty.objects.create(
                code=specialty["code"],
                title=specialty["title"],
            )

    for job in jobs:
        state = Vacancy.objects.create(
            title=job["title"],
            specialty=Specialty.objects.get(code=job["specialty"]),
            company=Company.objects.get(id=str(int(job["company"]) +16)),
            skills=job["skills"],
            description=job["description"],
            salary_min=job["salary_from"],
            salary_max=job["salary_to"],
            published_at=job["posted"],
        )
"""
import os
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'stepik_vacancies.settings'
django.setup()
from django.contrib.auth.models import User
from data import jobs, companies, specialties
from job_app.models import Vacancy, Company, Specialty

if __name__ == '__main__':
    for company in companies:
        state = Company.objects.update(
            owner=User.objects.get(id=1),
        )