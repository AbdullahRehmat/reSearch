FROM redis/redis-stack-server:latest 

WORKDIR /usr/local/db

COPY redis.conf ./redis.conf


CMD [ "redis-stack-server", "redis.conf" ]