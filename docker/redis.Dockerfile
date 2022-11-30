FROM alpine:edge

RUN apk update
RUN apk add --no-cache redis

COPY ./config/redis.conf /usr/local/etc/redis/redis.conf

EXPOSE 6379

CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
