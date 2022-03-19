FROM python:3.8.0-alpine

# Set working directory
WORKDIR /usr/src/app

# Python settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt .
RUN \
 apk add --no-cache python3 postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
#  apk add jpeg-dev zlib-dev libjpeg && \
 pip install --upgrade pip && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

# Working directory
COPY . .

# Start server  --> If deploying locally set port to whatever you like
CMD gunicorn blogengine.wsgi:application --preload --workers 3 --bind 0.0.0.0:$PORT