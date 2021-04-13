from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea

from job_app.models import Application, Company, Vacancy, Resume

CHOICES_STATUS = [('1', 'Ищу работу'), ('2', 'Рассматриваю предложения'), ('3', 'Не ищу работу')]
CHOICES_SPECIALTY = [
                    ('1', 'Backend developer'),
                    ('2', 'Frontend developer'),
                    ('3', 'Designer'),
                    ('3', 'Tester'),
                    ]
CHOICES_GRADE = [
                ('1', 'Trainee'),
                ('2', 'Junior'),
                ('3', 'Middle'),
                ('4', 'Senior'),
                ]


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')
        field_classes = {'username': UsernameField}

    username = forms.CharField(label='Логин', widget=TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=TextInput(attrs={'class': 'form-control'}))


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        field_classes = {'username': UsernameField}
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Исправьте логин или пароль и попробуйте снова.")
        return self.cleaned_data

    username = forms.CharField(label='Логин', widget=TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


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


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('name', 'surname', 'status', 'salary', 'specialty', 'grade', 'education', 'experience', 'portfolio')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'surname': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'custom-select mr-sm-2'}, choices=CHOICES_STATUS),
            'salary': forms.TextInput(attrs={'class': 'form-control'}),
            'specialty': forms.Select(attrs={'class': 'custom-select mr-sm-2'}, choices=CHOICES_SPECIALTY),
            'grade': forms.Select(attrs={'class': 'custom-select mr-sm-2'}, choices=CHOICES_GRADE),
            'education': forms.TextInput(attrs={'class': 'form-control'}),
            'experience': forms.Textarea(attrs={'class': 'form-control'}),
            'portfolio': forms.TextInput(attrs={'class': 'form-control'}),
        }
