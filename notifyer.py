from apscheduler.schedulers.blocking import BlockingScheduler
from backend.api.models import Userprofile, Stock
from backend.api.views import compute_D, compute_return
import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1) 
def timed_job():
    try:
        '''
        access to all User information and print all User's id and email address
        '''
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
                            expect_date = purchase_date + timedelta(days=user.invest_horizon*365//1)
                            a_s = compute_return(ps, p0, tax_s, hs)
                            a_l = compute_return(pl, p0, tax_l, left_horizon)
                            mail_tempelate = 'Dear user {}:\n   Your stock {} has reached a price of {:.2f}.The return from holding the security until {}, \
assuming it reached a price target of {:.2f}, would be {:.2%}. At the recent market price of {:.2f}, if you sell and invest the proceeds at your expected rate of return {:.2f}, \
your return from selling now is {:.2%}. Therefore, we advise selling now.'.format(user.user_name, s.name, ps, purchase_date.isoformat()[:10], pl, a_l, ps, s.expect_return_rate, a_s)
                            send_mail('Time to sell.',
                                    mail_tempelate,
                                    settings.EMAIL_HOST_USER,
                                    [user.email_address],
                                    fail_silently=False,)
                        s._sended = 1.0 
                    else:
                        s._sended = 0.0  
                    s.save()
            else:
                pass # No action
    except Exception as e:
        print("Something Wrong!")
        send_mail('Time to sell.',
        f'Exception{str(e)}',
        settings.EMAIL_HOST_USER,
        ['mooler0410@gmail.com'],
        fail_silently=False) 
    
sched.start()

