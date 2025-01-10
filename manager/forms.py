from django import forms
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import *


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

        labels = {
            'title': "",
            'description': ""
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Kurs nomini kiriting"
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Tavsifini kiriting"
            }),
        }

        error_messages = {
            'title': {
                'required': "Kurs nomini kiriting",
            }
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Course.objects.filter(title=title).exists():
            raise ValidationError("Ushbu kurs nomi allaqachon ishlatilgan.")

        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 1000:
            raise ValidationError("Tavsif matni uzunligi 1000 ta belgidan oshmasligi kerak.")
        elif len(description) < 5:
            raise ValidationError("Tavsif matni minimal 5 ta belgidan boshlanishi kerak.")

        return description


class RegisterForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email']
        labels = {
            'username': "Foydalanuvchi nomi",
            'email': "Elektron pochta manzili"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': "form-control form-control-lg"})
        self.fields['email'].widget.attrs.update({'class': "form-control form-control-lg"})
        self.fields['password1'].widget.attrs.update({'class': "form-control form-control-lg"})
        self.fields['password2'].widget.attrs.update({'class': "form-control form-control-lg"})


class LoginForm(AuthenticationForm):
    class Meta:
        model = MyUser
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        username = self.fields['username']
        password = self.fields['password']

        username.label = "Foydalanuvchi nomi"
        username.widget.attrs.update({'class': "form-control form-control-lg"})
        password.widget.attrs.update({'class': "form-control form-control-lg"})


class SettingsForm(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ['username', 'first_name', 'last_name', 'phone', 'email', 'photo']
        labels = {
            'username': "Foydalanuvchi nomi",
            'first_name': "Ism",
            'last_name': "Familiya",
            'phone': "Telefon raqam",
            'email': "Elektron pochta manzili",
            'photo': "Surat tanlang"

        }

        widgets = {
            'username': forms.TextInput(attrs={
                'class': "form-control",
                'readonly': 'readonly'
            }),

            'first_name': forms.TextInput(attrs={
                'class': "form-control",
            }),

            'last_name': forms.TextInput(attrs={
                'class': "form-control",
            }),

            'phone': forms.TextInput(attrs={
                'class': "form-control",
            }),

            'email': forms.EmailInput(attrs={
                'class': "form-control",
            }),

            'photo': forms.FileInput(attrs={
                'class': "form-control",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['phone'].required = False
        self.fields['photo'].required = False

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone and (not phone.isdigit() or len(phone) != 9):
            raise ValidationError("Telefon raqami noto'g'ri kiritildi.")

        return phone

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if first_name and not first_name.isalpha():
            raise ValidationError("Iltimos, faqat harflardan foydalaning!")

        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if last_name and not last_name.isalpha():
            raise ValidationError("Iltimos, faqat harflardan foydalaning!")

        return last_name


class PasswordForm(PasswordChangeForm):
    class Meta:
        model = MyUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        old_password = self.fields['old_password']
        new_password1 = self.fields['new_password1']
        new_password2 = self.fields['new_password2']

        old_password.label = "Amaldagi parol"
        old_password.widget.attrs.update({'class': "form-control"})
        new_password1.widget.attrs.update({'class': "form-control"})
        new_password2.widget.attrs.update({'class': "form-control"})


class EmailForm(forms.Form):
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': "form-control",
            'placeholder': "Sarlavha matnini kiriting"
        }),
        label=""
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': "form-control",
            'placeholder': "Xabar matnini kiriting"
        }),
        label=""
    )

    def clean_subject(self):
        subject = self.cleaned_data.get('subject')

        if len(subject) < 5:
            raise ValidationError("Sarlavha uzunligi kamida 5 ta belgidan iborat bo'lishi kerak.")
        elif len(subject) > 255:
            raise ValidationError("Sarlavha uzunligi 255 ta belgidan oshmasligi kerak.")

        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message')

        if len(message) < 5:
            raise ValidationError("Xabar matni uzunligi kamida 5 ta belgidan iborat bo'lishi kerak.")

        return message
