import redis

# to store revoked jwt tokens
access_blocklist = redis.StrictRedis(db=0, host="localhost", port=6379, decode_responses=True)
refresh_blocklist = redis.StrictRedis(db=1, host="localhost", port=6379, decode_responses=True)


# temp storage for PubNub sensor data
# dataset_id: [value, value, value...]
timestamp_list = redis.StrictRedis(db=2, host="localhost", port=6379, decode_responses=True)
heart_list = redis.StrictRedis(db=3, host="localhost", port=6379, decode_responses=True)
sweat_list = redis.StrictRedis(db=4, host="localhost", port=6379, decode_responses=True)
