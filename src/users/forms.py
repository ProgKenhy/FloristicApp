from django import forms

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from users.models import User
from users.tasks import send_email_verification
from django.db import models


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': "Введите пароль"}))

    class Meta:
        model = User



class UserRegisterForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': "Введите ваше имя"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': "Введите вашу фамилию"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'placeholder': "Введите адрес эл. почты"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': "Введите пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4',
        'placeholder': "Подтвердите пароль"}))


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=True)
        send_email_verification.delay(user.id)
        return user



class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))

   class Meta:
       model = User
       fields = ('first_name', 'last_name', 'email')