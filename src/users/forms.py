from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User, SexOptions
from users.tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control form-control-lg shadow-sm",
        'placeholder': "Введите имя пользователя"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg shadow-sm',
        'placeholder': "Введите пароль"}))

    class Meta:
        model = User


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-control-lg shadow-sm',
        'placeholder': "Имя",
        'max_length': 20}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control form-control-lg shadow-sm',
    #     'placeholder': "Фамилия"}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control form-control-lg shadow-sm",
        'placeholder': "Логин",
        'max_length': 20}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-control-lg shadow-sm',
        'placeholder': "Адрес эл. почты"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg shadow-sm',
        'placeholder': "Пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-control-lg shadow-sm',
        'placeholder': "Подтвердите пароль"}))

    class Meta:
        model = User
        fields = ('first_name', 'username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        # Вызов прямой отправки письма вместо Celery задачи
        send_email_verification(user.id)
        return user


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}))
    sex = forms.ChoiceField(
        choices=SexOptions.choices,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': "Выберите пол"}))
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': "Укажите ваш возраст"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'sex', 'age')
