FROM python:3.9-slim-buster
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install pipenv

WORKDIR /opt/app

COPY . ./

RUN pipenv install --system --dev

ENV FLASK_DEBUG=1
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run"]