import json
import os

import redis 
from dotenv import load_dotenv
import redis.client

# Path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")

# Clear the environment variables
os.environ.clear()

# Load environment variables from the .env file
load_dotenv(dotenv_path)

# Fetch AWS Redis credentials from the environment variables
aws_redis_endpoint = os.environ.get("AWS_REDIS_ENDPOINT")
aws_redis_port = os.environ.get("AWS_REDIS_PORT", 6379)
aws_redis_passsword = os.environ.get("AWS_REDIS_PASSWORD")

# Initialize the Redis client with AWS Redis endpoint.
redis_client = redis.Redis(
    host=aws_redis_endpoint,
    port=aws_redis_port,
    password=aws_redis_passsword,
    decode_responses=True
)

def insert_settings(app_id: str, new_settings: dict):

    # Convert settings dictionary to JSON string
    setttings_json= json.dumps(new_settings)

    # Insert JSON string in Reddis with app_id as the key
    redis_client.set(app_id, setttings_json)

def fetch_settings(app_id: str) -> dict:
    settings= redis_client.get(app_id)
    if settings:
        return json.loads(settings)
    return {}


