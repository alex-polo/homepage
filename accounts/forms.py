from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from accounts.models import ApplicationUser


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        fields = ('username', 'family_name', 'first_name', 'last_name', 'email', 'password1', 'password2')


class RegistrationUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username'}))
    family_name = forms.CharField(label='Фамилия', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'family_name'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'first_name'}))
    last_name = forms.CharField(label='Отчетство', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'last_name'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'email'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password'}))

    class Meta:
        model = ApplicationUser
        fields = ('username', 'family_name', 'first_name', 'last_name', 'email', 'password1', 'password2')
