FROM ubuntu:20.04

# set up ubuntu
ENV TZ=Europe/Dublin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt upgrade -y

RUN apt install -y build-essential \
   apache2 \
   libapache2-mod-wsgi-py3 \
   python3 \
   python3-dev \
   python3-pip \
   python3-venv \
   cron \
   openssl \
   ffmpeg \
   vim

RUN apt clean \
   && apt autoremove -y \
   && rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/moviology

# install pip requirements
COPY ./requirements.txt /var/www/moviology/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /var/www/moviology/requirements.txt

# configure apache
COPY ./server.conf /etc/apache2/sites-available/server.conf
RUN a2ensite server
RUN a2enmod headers

# Copy over the wsgi file
COPY ./server.wsgi /var/www/moviology/server.wsgi

RUN a2dissite 000-default.conf
RUN a2ensite server.conf

RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
   ln -sf /proc/self/fd/1 /var/log/apache2/error.log

EXPOSE 80

CMD  /usr/sbin/apache2ctl -D FOREGROUND

