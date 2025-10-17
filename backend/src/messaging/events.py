from fastapi import FastAPI
import json, os
from dotenv import load_dotenv
from datetime import datetime



def publish_event(app: FastAPI, event_type: str, data: dict):

    load_dotenv()
    RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "events")
    
    event = {
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data,
    }

    message = json.dumps(event)

    channel = app.state.rabbit_channel
    channel.basic_publish(
        exchange=RABBITMQ_EXCHANGE,
        routing_key=event_type, 
        body=message
    )

    print(f"Evento publicado: {message}")

