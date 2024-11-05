# import uuid
# from datetime import timedelta
#
# from celery import shared_task
# from django.utils.timezone import now
#
# from users.models import User, EmailVerification
#
#
# @shared_task
# def send_email_verification(user_id):
#     user = User.objects.get(id=user_id)
#     expiration = now() + timedelta(days=2)
#     record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
#     record.send_verification_email()


# utils.py или где у вас определен send_email_verification
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import uuid
from django.utils.timezone import now
from users.models import User, EmailVerification


def send_email_verification(user_id):
    user = User.objects.get(id=user_id)
    expiration = now() + timedelta(days=2)
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    record.send_verification_email()
