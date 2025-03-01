from kafka import KafkaConsumer
import json
from chat_bot.config.settings import config

class KafkaRequestConsumer:
    def __init__(self, request_handler):
        settings = config.get_kafka_config()
        self.consumer = KafkaConsumer(
            settings["topic_request"],
            bootstrap_servers=settings["servers"],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.request_handler = request_handler

    def consume_requests(self):
        for message in self.consumer:
            response = self.request_handler.process_request(message.value)
            print(f"Processed request: {message.value} -> Response: {response}")

if __name__ == "__main__":
    consumer = KafkaRequestConsumer()
    consumer.consume_requests()
