import pika
import json
import time
from datetime import datetime


class RabbitMQService:
    _connection = None
    _config = {}
    _executor = None

    @classmethod
    def load_config(cls, host, user, password, port=5672, executor=None):
        cls._config = {
            "host": host,
            "user": user,
            "password": password,
            "port": port,
        }
        cls._executor = executor
        print(f"🔌 RabbitMQ configuration loaded: {host}:{port} as {user}.")

    @classmethod
    def _create_connection(cls):
        """create connection with safe defaults."""
        credentials = pika.PlainCredentials(
            cls._config["user"], cls._config["password"]
        )
        params = pika.ConnectionParameters(
            host=cls._config["host"],
            port=cls._config["port"],
            credentials=credentials,
            heartbeat=30,  # keep connection alive
            blocked_connection_timeout=10,  # fail fast if blocked
            connection_attempts=3,
            retry_delay=3,
        )
        cls._connection = pika.BlockingConnection(params)
        return cls._connection

    @classmethod
    def _get_connection(cls):
        """Return an active connection, recreate if needed."""
        if cls._connection is None or cls._connection.is_closed:
            cls._connection = cls._create_connection()
        return cls._connection

    @classmethod
    def publish_event(cls, event_type: str, data: dict, retries: int = 3):
        """Publish an event with reconnection + retry logic."""
        for attempt in range(1, retries + 1):
            try:
                connection = cls._get_connection()
                channel = connection.channel()

                # Ensure exchange exists
                channel.exchange_declare(
                    exchange="events",
                    exchange_type="topic",
                    durable=True,
                )

                event = {
                    "event_type": event_type,
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": data,
                }

                channel.basic_publish(
                    exchange="events",
                    routing_key=event_type,
                    body=json.dumps(event),
                    properties=pika.BasicProperties(delivery_mode=2),
                )

                channel.close()
                print(f"✅ Event sent: {event_type}")
                return

            except (
                pika.exceptions.StreamLostError,
                pika.exceptions.ConnectionClosedByBroker,
                pika.exceptions.AMQPConnectionError,
            ) as e:
                print(f"⚠️ Connection lost: {e}. Retrying ({attempt}/{retries})...")
                cls._safe_close()
                time.sleep(2**attempt)  # exponential backoff

            except Exception as e:
                print(f"❌ Error sending event: {e}")
                cls._safe_close()
                break

        print(f"❌ Failed to send event after {retries} attempts: {event_type}")

    
    @classmethod
    def publish_event_async(cls, event_type: str, data: dict):
        if cls._executor:
            cls._executor.submit(cls.publish_event, event_type, data)
        else:
            cls.publish_event(event_type, data)

    @classmethod
    def _safe_close(cls):
        try:
            if cls._connection and not cls._connection.is_closed:
                cls._connection.close()
        except Exception:
            pass
        cls._connection = None

    @classmethod
    def close(cls):
        cls._safe_close()
        print("🔌 RabbitMQ connection closed.")

