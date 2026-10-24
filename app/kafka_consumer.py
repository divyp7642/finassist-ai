
import json
import os
import signal

from confluent_kafka import Consumer, KafkaException

from app.services.spending_summary_service import (
    process_transaction_spending
)


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "127.0.0.1:9092"
)

TOPIC = "transactions.created"

consumer = Consumer({
    "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    "broker.address.family": "v4",
    "group.id": "finassist-transaction-consumers",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
})

running = True


def stop_consumer(signum, frame):
    global running
    running = False


def process_transaction(event):
    transaction_data = event.get("data", event)
    transaction_id = transaction_data.get("transaction_id")

    if transaction_id is None:
        raise ValueError("Transaction ID is missing")

    print(
        f"Processing transaction {transaction_id}...",
        flush=True
    )

    # Update PostgreSQL spending summaries
    process_transaction_spending(event)

    print(
        f"Transaction {transaction_id} processed successfully",
        flush=True
    )


def start_consumer():
    consumer.subscribe([TOPIC])

    print(
        f"Listening for Kafka events on {TOPIC}...",
        flush=True
    )

    try:
        while running:
            message = consumer.poll(1.0)

            if message is None:
                continue

            if message.error():
                raise KafkaException(message.error())

            try:
                event = json.loads(
                    message.value().decode("utf-8")
                )

                process_transaction(event)

                # Commit only after database processing succeeds
                consumer.commit(
                    message=message,
                    asynchronous=False
                )

            except Exception as error:
                print(
                    f"Transaction processing failed: {error}",
                    flush=True
                )
                raise

    finally:
        consumer.close()
        print("Kafka consumer stopped.", flush=True)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, stop_consumer)
    signal.signal(signal.SIGTERM, stop_consumer)

    start_consumer()
