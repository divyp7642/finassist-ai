
import json
import os

from confluent_kafka import Producer
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Connect to Apache Kafka
# Windows default: 127.0.0.1:9092
# Docker: host.docker.internal:9092
producer = Producer({
    "bootstrap.servers": os.getenv(
        "KAFKA_BOOTSTRAP_SERVERS",
        "127.0.0.1:9092"
    ),
    "broker.address.family": "v4"
})


def publish_transaction_created(transaction_data):

    # Step 1: Create the event
    event = {
        "event": "transaction.created",
        "data": transaction_data
    }

    # Step 2: Convert the event to JSON bytes
    event_json = json.dumps(event).encode("utf-8")

    # Step 3: Track the delivery result
    delivery_status = {
        "success": False,
        "error": None
    }

    # Kafka calls this function when delivery finishes
    def delivery_report(err, msg):
        if err is not None:
            delivery_status["error"] = str(err)
            print(f"Kafka delivery failed: {err}")
        else:
            delivery_status["success"] = True
            print(
                f"Kafka message delivered to "
                f"{msg.topic()} [partition {msg.partition()}]"
            )

    # Step 4: Queue the event for Kafka
    producer.produce(
        topic="transactions.created",
        value=event_json,
        callback=delivery_report
    )

    # Step 5: Wait up to 10 seconds
    remaining = producer.flush(timeout=10)

    # Step 6: Check the delivery result
    if remaining > 0:
        raise RuntimeError(
            "Kafka message was not delivered within 10 seconds."
        )

    if not delivery_status["success"]:
        raise RuntimeError(
            f"Kafka delivery failed: {delivery_status['error']}"
        )
