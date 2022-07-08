FROM python:3.7


RUN apt-get update && apt-get -y upgrade

# supervisor installation &&
# create directory for child images to store configuration in
RUN apt-get -y install supervisor libpq-dev && \
  mkdir -p /var/log/supervisor && \
  mkdir -p /etc/supervisor/conf.d

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV MODEX_URI=http://51.144.180.220/
ENV MODEX_DATA_PORTS=""
ENV MODEX_AUTH_PORTS=""
ENV MODEX_TOKEN=""

COPY ./poetry.lock .
COPY ./pyproject.toml .

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

ADD supervisor.conf /etc/supervisor.conf
COPY . /app
WORKDIR /app

RUN python3 /app/console.py db init || true

CMD ["supervisord", "-c", "/etc/supervisor.conf"]
