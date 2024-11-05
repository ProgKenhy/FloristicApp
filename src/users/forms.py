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
        'placeholder': "Имя"}))
    # last_name = forms.CharField(widget=forms.TextInput(attrs={
    #     'class': 'form-control form-control-lg shadow-sm',
    #     'placeholder': "Фамилия"}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control form-control-lg shadow-sm",
        'placeholder': "Логин"}))
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
        fields = ('email', 'username', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        # Вызов прямой отправки письма вместо Celery задачи
        send_email_verification(user.id)
        return user


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    sex = forms.ChoiceField(
        choices=SexOptions.choices,
        widget=forms.Select(attrs={
            'class': 'form-control py-4',
            'placeholder': "Выберите пол"}))
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control py-4',
            'placeholder': "Укажите ваш возраст"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
