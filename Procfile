change_db: python manage.py makemigrations api
release: python manage.py migrate
cron: python manage.py corntab add  
web: gunicorn backend.wsgi --log-file -
