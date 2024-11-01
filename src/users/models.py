import uuid
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.core.mail import send_mail


class SexOptions(models.TextChoices):
    FEMALE = 'F', 'Female'
    MALE = 'M', 'Male'
    UNSURE = 'U', 'Unsure'


class User(AbstractUser):
    is_verified_email = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=False)
    sex = models.CharField(max_length=1, choices=SexOptions.choices)


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'Подтверждение электронной почты для {self.user.username}'
        message = (
            f'Для подтверждения учётной записи для {self.user.first_name} {self.user.last_name} перейдите по ссылке:'
            f' {verification_link}')
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        return now() >= self.expiration
