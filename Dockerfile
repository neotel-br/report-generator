# Use an official Python runtime as a parent image
FROM python:3.11.4-alpine3.17

# Install bash (if needed) and system dependencies for WeasyPrint
RUN apk add --no-cache --upgrade bash \
    gobject-introspection \
    cairo \
    pango \
    gdk-pixbuf \
    libxslt-dev \
    libxml2-dev \
    gcc \
    musl-dev \
    g++

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container

# Copy the requirements file into the container at /reports
COPY ./requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . ./reports

WORKDIR /reports

RUN mkdir /reports/results && chmod -R 755 /reports/results/

# Copy the rest of the application files into the container at /reports
RUN mkdir -p /usr/share/fonts/truetype/
RUN install -m644 ./static/fonts/Roboto-Regular.ttf /usr/share/fonts/truetype/
ENTRYPOINT ["python3", "main.py"]
