import pika, json, os, time
from dotenv import load_dotenv
from db import init_db, upsert_embedding
from model import generar_embedding, clasificar

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        uuid = data["uuid"]
        title = data.get("title", "")
        description = data.get("description", "")
        text = f"{title}. {description}"

        embedding = generar_embedding(text)
        category = clasificar(embedding)
        upsert_embedding(uuid, category, embedding)

        print(f"Job offer {uuid} → category: {category}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    init_db()

    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            channel = connection.channel()
            channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)

            print(f"Waiting for messages in queue '{RABBITMQ_QUEUE}'...")
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("Connection to RabbitMQ failed. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    main()
