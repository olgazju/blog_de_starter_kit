import random
import logging
import os
import json
import traceback

from confluent_kafka import KafkaError

from rp_handler import KafkaConsumer
from db_handler import DatabaseHandler


db = DatabaseHandler()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s :: %(levelname)s :: %(filename)s :: %(funcName)s :: %(message)s",
)

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


try:
    kafka_consumer_instance = KafkaConsumer(os.environ.get('BROKER_TOPIC', "my-topic"),
                                            os.environ.get('CONSUMER_GROUP', "my-group"))
    consumer = kafka_consumer_instance.consumer

    db = DatabaseHandler()

    while True:
        message = None
        msg_value = None

        try:
            message = consumer.poll(1.0)  # Poll for a message with a timeout of 1 second
            if message is None:
                #TODO: Implement reconnection if there is no more messages for a long time
                pass
            elif message.error():
                # Handle Kafka specific errors
                if message.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event - not an error
                    logger.info(f"Reached end of {message.topic()} at offset {message.offset()}")
                else:
                    logger.error(f"Error while consuming message: {message.error()}")
            else:
                # Handle the message
                msg_value = json.loads(message.value().decode('utf-8'))
                logger.info(f"Process message: {msg_value}")

                db.add_session(msg_value.get("user_id", random.randint(0, 1000)))

        except Exception as e:
            logger.error(f"Error: {str(e)}.")
            logger.error(traceback.format_exc())


except KeyboardInterrupt:
    logger.info("Interrupt received, shutting down gracefully.")
    
finally:
    consumer.close()
