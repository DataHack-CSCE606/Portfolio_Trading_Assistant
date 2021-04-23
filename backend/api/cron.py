from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import Message, MessageSerializer
from .models import *

from django.shortcuts import *
from .models import UserProfile
from .forms import ProfileForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def my_task():
    '''
    access to all User information and print all User's id and email address
    '''
    all_user = User.objects.all()
    for user in all_user:
        print(user.id, ' : ', user.email)
        #send_email
        print('================sender email adrress: ', settings.EMAIL_HOST_USER)
        send_mail('EMAIL NOTIFICATION TEST',
                'HI, this is an email notification test per 1 min',
                settings.EMAIL_HOST_USER,
                [user.email, 'qf31@tamu.edu'],
                fail_silently=False,)
