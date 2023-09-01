import os
import logging
import json
from confluent_kafka import Consumer, Producer

logger = logging.getLogger(__name__)

DEFAULT_KAFKA_URL = "localhost:19092"

class KafkaConsumer:
    def __init__(self, broker_topic, consumer_group):
        # Retrieve settings from the environment
        self.broker_url = os.environ.get('BROKER_URL', DEFAULT_KAFKA_URL)
        self.broker_topic = broker_topic
        self.consumer_group = consumer_group

        self.kafka_config = {
            'bootstrap.servers': self.broker_url,
            'group.id': self.consumer_group,
            'enable.auto.commit': False,
            'auto.offset.reset': "earliest",
            'default.topic.config': {'auto.offset.reset': 'earliest'}
        }

        self.consumer = self.create_consumer()

    def create_consumer(self):
        """Creates and returns a Kafka consumer."""
        consumer = Consumer(self.kafka_config)
        consumer.subscribe([self.broker_topic])
        logger.info(f"Created consumer with config: {self.kafka_config} that listens to {self.broker_topic}")
        return consumer


class KafkaProducer:
    def __init__(self, topic_name: str, client_id: str):
        self.broker_url = os.environ.get('BROKER_URL', DEFAULT_KAFKA_URL)
        self.topic_name = topic_name
        self.client_id = client_id
        self.conf = {
            'bootstrap.servers': self.broker_url,
            'client.id': self.client_id
        }
        self.producer = Producer(self.conf)

    def __delivery_report(self,err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). 
        """
        if err is not None:
            logger.error('Message delivery failed: {}'.format(err))
        else:
            logger.info('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def send_messages(self, messages):
        for message in messages:
            json_message = json.dumps(message)
            logger.info(f"Produce {json_message} to topic {self.topic_name} on {self.broker_url}")
            self.producer.produce(self.topic_name, json_message, callback=self.__delivery_report)
        self.producer.flush()
