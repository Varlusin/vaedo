FROM python:3.11-slim

WORKDIR /vaedo

RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    libpq-dev \
    gcc \
    build-essential \ 
    && rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV PYTHONPATH=/vaedo
ENV DJANGO_SETTINGS_MODULE=vaedo.settings

COPY requirements.txt /vaedo/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install "django-allauth[socialaccount]"
RUN pip install "django-environ"
RUN pip install "django-cors-headers"
RUN pip install "djangorestframework-gis"


COPY . /vaedo



EXPOSE 8000
