import pika, json, os, time, asyncio
from dotenv import load_dotenv
from db import init_db, upsert_embedding
from model import generate_embedding, classify_embedding

def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        data = message.get("data", {})

        print(f"Data {data}")

        #id = data["id"]
        #title = data.get("title", "")
        #description = data.get("description", "")
        #text = f"{title}. {description}"

        #embedding = generate_embedding(text)
        #category = classify_embedding(embedding)
        #upsert_embedding(id, category, embedding)

        ch.basic_ack(delivery_tag=method.delivery_tag)

        print(f"Job offer {message}")

    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)



def connect_to_rabbitmq(RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_QUEUE):

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
    load_dotenv()

    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
    RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE", "job_events_queue")

    while True:
        try:
            connection, channel = connect_to_rabbitmq(
                RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_QUEUE
            )

            # 🧩 Estas 3 declaraciones deben ir antes del consumo
            channel.exchange_declare(
                exchange='events',
                exchange_type='topic',
                durable=True
            )

            channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

            channel.queue_bind(
                queue=RABBITMQ_QUEUE,
                exchange='events',
                routing_key='job.*'
            )

            # Ahora sí puedes consumir
            channel.basic_consume(
                queue=RABBITMQ_QUEUE,
                on_message_callback=callback,
                auto_ack=False  # o True según tu lógica
            )

            print(f"✅ Conectado a RabbitMQ. Esperando mensajes en '{RABBITMQ_QUEUE}'...")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("❌ Conexión a RabbitMQ falló. Reintentando en 5 segundos...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("👋 Saliendo...")
            try:
                channel.stop_consuming()
                connection.close()
            except Exception:
                pass
            sys.exit(0)
        except Exception as e:
            print(f"⚠️ Error inesperado: {e}")
            try:
                if channel.is_open:
                    channel.stop_consuming()
                if connection.is_open:
                    connection.close()
            except Exception:
                pass
            print("Reintentando en 5 segundos...")
            time.sleep(5)

if __name__ == "__main__":
    main()