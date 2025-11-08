import pika, json, os, time
from dotenv import load_dotenv
from db import init_db
from model import init_embedding, process_job_data, recommend_jobs



def jobs_callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        job_data = message.get("data", {})
        process_job_data(job_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)



def profiles_callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        profile_data = message.get("data", {})
        recommend_jobs(profile_data)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)



def connect_to_rabbitmq(RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD):

    """Attempt to connect and return a channel"""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            port=5672,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        )
    )
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)
    return connection, channel



def run_worker():
    init_db()
    init_embedding()
    load_dotenv()

    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
    RABBITMQ_USER = os.getenv("RABBITMQ_USER")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")


    while True:
        try:
            connection, channel = connect_to_rabbitmq(
                RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD
            )

            channel.exchange_declare(exchange='events', exchange_type='topic', durable=True)

            channel.queue_declare(queue="job_events_queue", durable=True)
            channel.queue_bind(queue="job_events_queue", exchange='events', routing_key='job.*')

            channel.queue_declare(queue="profiles_events_queue", durable=True)
            channel.queue_bind(queue="profiles_events_queue", exchange='events', routing_key='profile.*')

            channel.basic_consume(queue="job_events_queue", on_message_callback=jobs_callback, auto_ack=False)
            channel.basic_consume(queue="profiles_events_queue", on_message_callback=profiles_callback, auto_ack=False)

            print(f"✅ Connected to RabbitMQ. Waiting for messages in 'job_events_queue' and 'profiles_events_queue'...")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("❌ Connection to RabbitMQ failed. Retrying in 5 seconds...")
            time.sleep(5)
        
        except KeyboardInterrupt:
            print("👋 Exiting...")
            try:
                channel.stop_consuming()
                connection.close()
            except Exception:
                pass
            sys.exit(0)
        
        except Exception as e:
            print(f"⚠️ Unexpected error: {e}")
            try:
                if channel.is_open:
                    channel.stop_consuming()
                if connection.is_open:
                    connection.close()
            except Exception:
                pass
            print("Retrying in 5 seconds...")
            time.sleep(5)
