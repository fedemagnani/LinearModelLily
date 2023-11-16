
FROM python:3.10.10-buster

# RUN apk add --no-cache --update \
#     python3 python3-dev gcc \
#     gfortran musl-dev g++ \
#     libffi-dev openssl-dev \
#     libxml2 libxml2-dev \
#     libxslt libxslt-dev \
#     libjpeg-turbo-dev zlib-dev

RUN pip install --upgrade cython

### install python dependencies if you have some
RUN pip3 install requests==2.25.1
RUN pip3 install pandas

RUN pip3 install -U scikit-learn --no-cache-dir

### We make sure that we have authorizations to write on /tmp
RUN chmod 777 -R /tmp && chmod o+t -R /tmp 

# Copy the current directory contents into the container
COPY ./src /app

#tun the app
ENTRYPOINT ["python3", "/app/app.py"]

# # Set the working directory in the container
# WORKDIR /app

# # COPY . /app
# FROM ubuntu
# # ...
# ENV DEBIAN_FRONTEND noninteractive
# RUN apt-get update && \
#     apt-get -y install gcc mono-mcs && \
#     rm -rf /var/lib/apt/lists/*
