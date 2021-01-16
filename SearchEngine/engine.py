import redis
from rank_bm25 import BM25Okapi

redis_host = "redis-api"
redis_port = 6379
redis_password = "Password:)"

# Connect to Redis Streams

r1 = redis.Redis(host=redis_host, port=redis_port,
                 password=redis_password, db=1, decode_responses=True)


global msg

while True:
    msg = r1.xread({'streamOne': "$"}, count=1, block=0)
    print(msg)

# Connects to ContentScraper Database

# Parses Query from Stream
query = "QuestionFromSite"

# Data
query = query
urls = {
    '1': 'http://www.aboutatheism.net/'
}


# BM25

# Returns Results