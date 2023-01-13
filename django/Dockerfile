# base used for development
FROM python:3.11 as base

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash", "-c", "sleep ${DJANGO_DELAY:-3}; python manage.py migrate; python manage.py createsuperuser --noinput; python manage.py runserver 0.0.0.0:8000"]

# prod used for what we call production
FROM base as prod
# ENV DJANGO_DELAY=3
# ENV DJANGO_SUPERUSER_USERNAME=admin
# ENV DJANGO_SUPERUSER_PASSWORD=admin
# ENV DJANGO_SUPERUSER_EMAIL=admin@example.com

COPY . .

CMD ["/bin/bash", "-c", "sleep ${DJANGO_DELAY:-3}; python manage.py migrate; python manage.py createsuperuser --noinput; python manage.py check --deploy; python manage.py runserver 0.0.0.0:8000"]