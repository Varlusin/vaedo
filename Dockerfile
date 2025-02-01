FROM python:3.8-slim

WORKDIR /vaedo

RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

COPY requirements.txt /vaedo/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /vaedo


EXPOSE 8000
