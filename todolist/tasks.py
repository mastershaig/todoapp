# from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model




# Use celery shared_task documentation here
# http://docs.celeryproject.org/en/latest/faq.html
@shared_task
def send_notification(a):
    # get first Investor list
    User = get_user_model()
    user = User.objects.get(id=a)
    send_mail('Your todoapp is expiring in 10 mins', 'Hey, your todoapp is expiring in 10 mins', 'mast3rdev@gmail.com',
              [user.email])
    print("Notification Sent")
    return "Done"
