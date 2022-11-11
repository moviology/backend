FROM ubuntu:20.04

#################
# set up ubuntu #
#################
ENV TZ=Europe/Dublin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt update && apt upgrade -y

RUN apt install -y build-essential \
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

RUN service nginx restart \
   && nginx -s reload -t \
   && nginx -s reload


#####################
# set up supervisor #
#####################
RUN rm -f /etc/supervisor/conf.d/* \
   && mkdir /var/log/api \
   && touch /var/log/api/api.out.log \
   && touch /var/log/api/api.err.log

COPY ./config/supervisor.conf /etc/supervisor/conf.d/supervisor.conf

RUN ln -sf /proc/self/fd/1 /var/log/api/api.out.log \
   && ln -sf /proc/self/fd/1/var/log/api/api.err.log 


#############
# start app #
#############
EXPOSE 80
COPY ./ /home/backend
WORKDIR /home/backend
CMD gunicorn -w 3 api:app -b :80
