import redis.asyncio as redis
import os


class BaseManager:
    def __init__(self):
        """
        Initialize the BaseManager.

        This class provides a base for managing data using Redis.

        Initializes a connection to the Redis server.

        Attributes:
            redis (redis.StrictRedis): A connection to the Redis server.
        """
        self.redis = redis.StrictRedis(
            host=os.environ.get("DB_HOST", "localhost"),
            port=6379,
            db=0,
            decode_responses=True,
        )

    async def close(self):
        """
        Close the connection to the Redis server.

        This method is used to close the connection when it's no longer needed.
        """
        await self.redis.close()
