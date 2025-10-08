import pika, json, os, time
from dotenv import load_dotenv
from db import init_db, upsert_embedding
from model import generate_embedding, classify_embedding

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        uuid = data["uuid"]
        title = data.get("title", "")
        description = data.get("description", "")
        text = f"{title}. {description}"

        embedding = generate_embedding(text)
        category = classify_embedding(embedding)
        upsert_embedding(uuid, category, embedding)

        print(f"Job offer {uuid} → category: {category}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)



def connect_to_rabbitmq():
    """Attempt to connect and return a channel"""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=5672,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_qos(prefetch_count=1)
    return connection, channel



def main():
    init_db()

    while True:
        try:
            connection, channel = connect_to_rabbitmq()
            channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
            print(f"Connected to RabbitMQ. Waiting for messages in queue '{RABBITMQ_QUEUE}'...")
            channel.start_consuming()
        except pika.exceptions.AMQPConnectionError:
            print("Connection to RabbitMQ failed. Retrying in 5 seconds...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("Shutting down...")
            try:
                channel.stop_consuming()
                connection.close()
            except Exception:
                pass
            sys.exit(0)
        except Exception as e:
            print(f"Unexpected error: {e}")
            try:
                if channel.is_open:
                    channel.stop_consuming()
                if connection.is_open:
                    connection.close()
            except Exception:
                pass
            print("Reconnecting in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    main()