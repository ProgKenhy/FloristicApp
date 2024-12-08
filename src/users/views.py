from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import TemplateView

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from users.models import User, EmailVerification


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')
    title = 'Авторизация'


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегистрированы!'
    title = 'Регистрация'


class UserProfileView(UpdateView):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    title = 'Профиль'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=[self.object.id])


class EmailVerificationView(TemplateView):
    title = 'Подтверждение почты'
    template_name = 'users/password/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password/password_reset.html'
    email_template_name = 'users/password/password_reset_email.html'
    subject_template_name = 'users/password/password_reset_subject.txt'
    success_message = ("Мы отправили вам по электронной почте инструкции по установке пароля, если существует учетная"
                       " запись с указанным вами адресом электронной почты. Вы должны получить их в ближайшее время."
                       " Если вы не получили электронное письмо, Пожалуйста, убедитесь, что вы правильно ввели адрес,"
                       " под которым зарегистрировались, и проверьте папку со спамом.")
    success_url = reverse_lazy('users:login')



