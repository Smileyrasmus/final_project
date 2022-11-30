FROM python:3.11

ENV DJANGO_DELAY=3

ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["/bin/bash", "-c", "sleep ${DJANGO_DELAY}; python manage.py migrate; python manage.py createsuperuser --noinput; python manage.py runserver 0.0.0.0:8000"]