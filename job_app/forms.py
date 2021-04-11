from django import forms
from django.forms import ModelForm, TextInput, Textarea
from job_app.models import Application, Company, Vacancy
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')

    first_name = forms.CharField(label='Имя', widget=TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Логин', widget=TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    username = forms.CharField(label='Логин', widget=TextInput)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')
        widgets = {
            'written_cover_letter': Textarea(attrs={'class': 'form-control'}),
            'written_username': TextInput(attrs={'class': 'form-control'}),
            'written_phone': TextInput(attrs={'class': 'form-control'}),
        }


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'logo', 'employee_count', 'location', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'custom-file-input', 'multiple data-min-file-count': '0'}),
            'employee_count': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('title', 'specialty', 'salary_min', 'salary_max', 'skills', 'description')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'specialty': forms.Select(attrs={'class': 'custom-select mr-sm-2'}),
            'salary_min': forms.TextInput(attrs={'class': 'form-control'}),
            'salary_max': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        }
