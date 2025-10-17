import pika, os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "events")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

def setup_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    ))
    channel = connection.channel()

    # 1. Crear el exchange tipo topic
    exchange_name = RABBITMQ_EXCHANGE
    channel.exchange_declare(exchange=exchange_name, exchange_type="topic", durable=True)

    # 2. Declarar colas
    channel.queue_declare(queue="profile_events_queue", durable=True)
    channel.queue_declare(queue="job_events_queue", durable=True)
    
    # 3. Bindings (enlaces)
    channel.queue_bind(
        exchange=exchange_name, queue="profile_events_queue", routing_key="profile.*"
    )
    channel.queue_bind(
        exchange=exchange_name, queue="job_events_queue", routing_key="job.*"
    )

    print("Exchange y bindings configurados correctamente")
    connection.close()
