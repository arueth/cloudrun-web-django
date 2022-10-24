FROM python:3.10-slim-bullseye as build-stage

ENV PATH=/venv/bin:${PATH}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get -y update \
&& apt-get -y install gcc libpq-dev \
&& pip install --upgrade pip \
&& python -m venv /venv

COPY requirements.txt /venv/requirements.txt

RUN pip install --no-cache-dir -r /venv/requirements.txt


FROM python:3.10-slim-bullseye as final-stage

ENV PATH=/venv/bin:${PATH}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=build-stage /venv /venv

WORKDIR /app

RUN apt-get -y update \
&& apt-get -y install libpq-dev \
&& apt-get clean

COPY src /app
COPY bin/ /

ENV PORT=8080

ENTRYPOINT ["/entrypoint.sh"]
#CMD python manage.py runserver 0.0.0.0:${PORT}
CMD gunicorn --bind 0.0.0.0:${PORT} --threads 8 --workers 1  website.wsgi