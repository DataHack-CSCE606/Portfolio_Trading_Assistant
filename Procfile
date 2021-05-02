change_db: python manage.py makemigrations api
release: python manage.py migrate
cron: python manage.py crontab add  
web: gunicorn backend.wsgi --log-file -
