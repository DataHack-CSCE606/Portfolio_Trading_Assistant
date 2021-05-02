from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from .models import Message, MessageSerializer
from .models import Userprofile, Stock

from django.shortcuts import *
from .models import UserProfile
from .views import compute_D. compute_return
from .forms import ProfileForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
import yfinance as yf





def my_task():
    '''
    access to all User information and print all User's id and email address
    '''
    try:
        all_user = Userprofile.objects.all()
        for user in all_user:
            print(user.user_id, ' : ', user.email_address)
            if user.sell_notify > 0:
                opp_r = user.opportunity_cost
                tax_s = user.short_tax_rate
                tax_l = user.long_tax_rate  # by dafault.
                full_horizon = user.invest_horizon
                #send_email
                for s in user.stocks.all():
                    s_code = s.code
                    yf_stock = yf.Ticker(s_code)
                    purchase_date = s.purchase_date
                    p0 = s.purchase_price 
                    pl = s.target_price
                    ps = yf_stock.history(period='1d')["Close"][0]
                    hs = ((timezone.now() - purchase_date).days) / 365     # in year
                    left_horizon = full_horizon - hs if (full_horizon - hs) > 0 else 0
                    close_date = yf_stock.history(period='1d').index[0].isoformat()[:10]
                    D = compute_D(tax_l, tax_s, pl, ps, p0, opp_r, left_horizon, hs)
                    if D < 0:
                        if s._sended < 1.:
                            expect_date = purchase_date + timedelta(days=user.investment_horizon*365//1)
                            a_s = compute_return(ps, p0, tax_s, hs),
                            a_l = compute_return(pl, p0, tax_l, left_horizon),
                            mail_tempelate = 'Dear user {}:\n   Your stock {} has reached a price of {}.The return from holding the security until {}, \
assuming it reached a price target of {}, would be {}%. At the recent market price of {}, if you sell and invest the proceeds at your expected rate of return {}, \
your return from selling now is {}%. Therefore, we advise selling now.'.format(user.user_name, s.name, ps, purchase_date, pl, a_l, ps, s.expect_return_rate, a_s)
                            send_mail('Time to sell.',
                                    mail_tempelate,
                                    settings.EMAIL_HOST_USER,
                                    [user.email],
                                    fail_silently=False,)
                        s._sended = 1.0 
                    else:
                        s._sended = 0.0  
                    s.save()
            else:
                pass # No action
    except Exception as e:
        send_mail('SELL NOTIFICATION',
                  f'{str(e)}',
                  settings.EMAIL_HOST_USER,
                  [user.email],
                  fail_silently=False,)
