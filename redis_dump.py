#!/usr/bin/env python3
"""
Dump a redis key (hash or stream) to JSON file.
"""
import json
import os
from pathlib import Path

import sys

try:
    import redis
except ImportError:
    print("redis is not installed. Please install it via: pip install redis")
    sys.exit(1)


REDIS_HOST = "localhost"
REDIS_PORT = 6379


def get_redis():
    """
    Create a Redis client with host and port which can be either provided via
    environment variables or the default ones.
    """
    host = os.environ.get("REDIS_HOST", REDIS_HOST)
    port = os.environ.get("REDIS_PORT", REDIS_PORT)
    R = redis.StrictRedis(host=host, port=port, decode_responses=True)
    if not R.ping():
        print(f"Failed to connect to Redis server on {host}:{port}")
        return None
    return R


def get_hash_content(redis_client: redis.Redis, key: str) -> dict[str, str]:
    assert redis_client.type(key) == 'hash'
    data = redis_client.hgetall(key)
    return data


def get_stream_content(redis_client: redis.Redis, key: str) -> dict[str, str]:
    assert redis_client.type(key) == 'stream'
    data = redis_client.xrevrange(key)
    return data


def main(key):
    if (R :=  get_redis()) is None:
        sys.exit(1)

    match R.type(key):
        case "hash":
            data = get_hash_content(R, key)
        case "stream":
            data = get_stream_content(R, key)
        case 'none':
            print('Specified key does not exist')
            sys.exit(1)
        case _:
            print('Only support hash and stream')
            sys.exit(1)

    json_fpath = Path.cwd() / f"{key}.json"
    data_str = json.dumps(data, indent="  ")
    json_fpath.write_text(data_str)
    print(f"Successfully dumpped data to {json_fpath}")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print(f'Usage:\n\t{sys.argv[0]} key')
