FROM ubuntu:20.04

#################
# set up ubuntu #
#################
ENV TZ=Europe/Dublin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt upgrade -y

RUN apt install -y build-essential \
   systemctl \
   nginx \
   python3 \
   python3-dev \
   python3-pip \
   python3-venv \
   gunicorn \
   supervisor \
   openssl \
   ffmpeg \
   vim

RUN apt clean \
   && apt autoremove -y \
   && rm -rf /var/lib/apt/lists/*


############################
# install pip requirements #
############################
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt


###############
# setup nginx #
###############
RUN rm -f /etc/nginx/sites-enabled/default \
   && rm -f /etc/nginx/conf.d/default.conf

COPY ./config/nginx.conf /etc/nginx/conf.d/nginx.conf


#####################
# set up supervisor #
#####################
RUN rm -f /etc/supervisor/conf.d/* \
   && mkdir -p /var/log/supervisor \
   && touch /var/log/supervisor/api.out.log \
   && touch /var/log/supervisor/api.err.log

COPY ./config/supervisor.conf /etc/supervisor/conf.d/supervisor.conf


###################
# display logfile #
###################
#! Not working
RUN ln -sf /proc/self/fd/1 /var/log/gunicorn/access.log \
   && ln -sf /proc/self/fd/2 /var/log/gunicorn/error.log


######################
# copy project files #
######################
EXPOSE 80
COPY ./ /home/backend
WORKDIR /home/backend