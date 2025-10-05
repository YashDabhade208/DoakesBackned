"""
Redis client for caching and session management.
"""

import redis
import json
import logging
from typing import Optional, Any, Dict
from app.config import settings

logger = logging.getLogger(__name__)


class RedisClient:
    """Redis client wrapper for caching and session management."""

    def __init__(self):
        self.client = None
        self.is_connected = False
        self._connect()

    def _connect(self):
        """Establish connection to Redis."""
        try:
            self.client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password,
                decode_responses=True
            )
            # Test the connection
            self.client.ping()
            self.is_connected = True
            logger.info("Connected to Redis successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            self.is_connected = False

    def get(self, key: str) -> Optional[str]:
        """Get value from Redis."""
        if not self.is_connected or not self.client:
            return None

        try:
            return self.client.get(key)
        except Exception as e:
            logger.error(f"Error getting key {key}: {str(e)}")
            return None

    def set(self, key: str, value: Any, expire: Optional[int] = None) -> bool:
        """Set value in Redis."""
        if not self.is_connected or not self.client:
            return False

        try:
            serialized_value = json.dumps(value) if not isinstance(value, str) else value
            if expire:
                return bool(self.client.setex(key, expire, serialized_value))
            else:
                return bool(self.client.set(key, serialized_value))
        except Exception as e:
            logger.error(f"Error setting key {key}: {str(e)}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from Redis."""
        if not self.is_connected or not self.client:
            return False

        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Error deleting key {key}: {str(e)}")
            return False

    def exists(self, key: str) -> bool:
        """Check if key exists in Redis."""
        if not self.is_connected or not self.client:
            return False

        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Error checking key {key}: {str(e)}")
            return False

    def set_json(self, key: str, data: Dict, expire: Optional[int] = None) -> bool:
        """Set JSON data in Redis."""
        return self.set(key, data, expire)

    def get_json(self, key: str) -> Optional[Dict]:
        """Get JSON data from Redis."""
        value = self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                logger.error(f"Error decoding JSON for key {key}")
                return None
        return None

    def publish(self, channel: str, message: Any) -> bool:
        """Publish message to Redis channel."""
        if not self.is_connected or not self.client:
            return False

        try:
            serialized_message = json.dumps(message) if not isinstance(message, str) else message
            return bool(self.client.publish(channel, serialized_message))
        except Exception as e:
            logger.error(f"Error publishing to channel {channel}: {str(e)}")
            return False

    def subscribe(self, channel: str):
        """Subscribe to Redis channel."""
        if not self.is_connected or not self.client:
            return None

        try:
            pubsub = self.client.pubsub()
            pubsub.subscribe(channel)
            return pubsub
        except Exception as e:
            logger.error(f"Error subscribing to channel {channel}: {str(e)}")
            return None

    def reconnect(self):
        """Reconnect to Redis."""
        self.is_connected = False
        self.client = None
        self._connect()

    def health_check(self) -> Dict[str, Any]:
        """Check Redis health."""
        return {
            "connected": self.is_connected,
            "host": settings.redis_host,
            "port": settings.redis_port,
            "db": settings.redis_db
        }
