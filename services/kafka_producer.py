from kafka import KafkaProducer
import json
from chat_bot.config.settings import config

class KafkaResponseProducer:
    def __init__(self):
        settings = config.get_kafka_config()
        self.producer = KafkaProducer(
            bootstrap_servers=settings["servers"],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        # Используем переданный топик или значение по умолчанию из конфигурации
        self.topic_response = settings["topic_response"]

    def send_response(self, response_data):
        """Отправляет ответ в Kafka топик, установленный при инициализации."""
        self.producer.send(self.topic_response, value=response_data)
        self.producer.flush()

# Пример использования
if __name__ == "__main__":
    # Создаем экземпляр KafkaResponseProducer с кастомным топиком
    producer = KafkaResponseProducer()
    producer.send_response({"user_id": "123", "response": "Привет!"})
