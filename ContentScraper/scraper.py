# Import Modules
import redis
import scrapy

# Connect to Redis Streams
redis_host = "redis-api"
redis_port = 6379
redis_password = "Password:)"

r1 = redis.Redis(host=redis_host, port=redis_port,
                password=redis_password, db=1, decode_responses=True)


# Connect to DB


# Scrapy Script


# Save Output to DB