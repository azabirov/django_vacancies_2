from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=120)
    location = models.CharField(max_length=120)
    logo = models.ImageField(
                             upload_to='MEDIA_COMPANY_IMAGE_DIR',
                             height_field='height_field',
                             width_field='width_field',
                             default='100x60.gif',
                             blank=True,
                             )
    height_field = models.PositiveIntegerField(default=60, null=True)
    width_field = models.PositiveIntegerField(default=100, null=True)
    description = models.TextField()
    employee_count = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True, blank=True)

    def __str__(self):
        return self.name


class Specialty(models.Model):
    code = models.CharField(max_length=32)
    title = models.CharField(max_length=120)
    picture = models.ImageField(
                                upload_to='MEDIA_SPECIALITY_IMAGE_DIR',
                                height_field='height_field',
                                width_field='width_field',
                                default='100x60.gif',
                                )
    height_field = models.PositiveIntegerField(default=60)
    width_field = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.code


class Vacancy(models.Model):
    title = models.CharField(max_length=120)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.TextField()
    description = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    written_username = models.CharField(max_length=120, verbose_name='Ваше имя')
    written_phone = models.CharField(max_length=16, verbose_name='Ваш телефон')
    written_cover_letter = models.TextField(verbose_name='Сопроводительное письмо')
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications", default=None)

    def __str__(self):
        return self.written_username


class Resume(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=40)
    status = models.CharField(max_length=30)
    salary = models.CharField(max_length=8)
    specialty = models.CharField(max_length=64)
    grade = models.CharField(max_length=64)
    education = models.CharField(max_length=64)
    experience = models.CharField(max_length=64)
    portfolio = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resume_owner', null=True, blank=True)

    def __str__(self):
        return self.name
