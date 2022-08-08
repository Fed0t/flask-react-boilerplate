FROM python:3.7


RUN apt-get update && apt-get -y upgrade

# supervisor installation &&
# create directory for child images to store configuration in
RUN apt-get -y install supervisor libpq-dev && \
  mkdir -p /var/log/supervisor && \
  mkdir -p /etc/supervisor/conf.d

ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV FLASK_ENV=development

ADD supervisor.conf /etc/supervisor.conf
COPY . /wallets

RUN pip install -r /wallets/requirements.txt

WORKDIR /wallets

RUN python3 /app/console.py db init || true

CMD ["supervisord", "-c", "/etc/supervisor.conf"]
