from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class SexOptions(models.TextChoices):
    FEMALE = 'F', 'Female'
    MALE = 'M', 'Male'
    UNSURE = 'U', 'Unsure'


class User(AbstractUser):
    is_verified_email = models.BooleanField(default=False)
    email = models.EmailField(unique=True, blank=False)
    sex = models.CharField(max_length=1, choices=SexOptions.choices)
    age = models.PositiveIntegerField(null=True, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.email


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True)
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
            f'Для подтверждения учётной записи для {self.user.username} перейдите по ссылке:'
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


