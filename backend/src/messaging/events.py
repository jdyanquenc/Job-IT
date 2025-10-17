import pika, json, os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "events")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

def publish_event(event_type: str, data: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=5672,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        )
    )
    channel = connection.channel()

    exchange_name = RABBITMQ_EXCHANGE
    channel.exchange_declare(
        exchange=exchange_name, exchange_type="topic", durable=True
    )

    event = {
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
    }

    message = json.dumps(event)

    channel.basic_publish(
        exchange=exchange_name,
        routing_key=event_type, 
        body=message,
        properties=pika.BasicProperties(delivery_mode=2),  # Persistente
    )

    print(f"Evento publicado: {message}")
    connection.close()
