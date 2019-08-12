from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging

logger=logging.getLogger()

producer = KafkaProducer(bootstrap_servers=['10.66.216.17:9092'])
try:
    producer.send (topic)
except KafkaError:
    logger.info("Can't send data to Kafka")