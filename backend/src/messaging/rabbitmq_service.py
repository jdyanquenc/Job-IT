import pika, json
from datetime import datetime


# rabbitmq_service.py
class RabbitMQService:
    _connection = None
    _channel = None
    _config = {}

    @classmethod
    def load_config(cls, host, user, password, port):
        cls._config = {"host": host, "user": user, "password": password, "port": port}

    @classmethod
    def connect(cls):
        if not cls._config:
            raise Exception("RabbitMQService config no cargada")

        if cls._connection is None or cls._connection.is_closed:
            credentials = pika.PlainCredentials(
                cls._config["user"], cls._config["password"]
            )
            params = pika.ConnectionParameters(
                host=cls._config["host"],
                port=cls._config["port"],
                credentials=credentials,
            )
            cls._connection = pika.BlockingConnection(params)
            cls._channel = cls._connection.channel()

    @classmethod
    def publish_event(cls, event_type: str, data: dict):
        cls.connect()  # asegura conexión activa
        event = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        cls._channel.basic_publish(
            exchange='events',
            routing_key=event_type,
            body=json.dumps(event)
        )
        print(f"Evento enviado: {event_type}")

    @classmethod
    def close(cls):
        if cls._connection and not cls._connection.is_closed:
            cls._connection.close()
            print("RabbitMQ cerrado")
