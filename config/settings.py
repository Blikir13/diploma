class Config:
    """Базовый класс конфигурации, содержащий настройки системы."""

    def __init__(self):
        # Настройки ClickHouse
        self.CLICKHOUSE_HOST = "localhost"
        self.CLICKHOUSE_DB = "chatbot"

        # Настройки Kafka
        self.KAFKA_SERVERS = ["localhost:9092"]
        self.KAFKA_TOPIC = "chatbot_requests"
        self.KAFKA_TOPIC_RESPONSE = "chatbot_responses"

    def get_clickhouse_config(self):
        """Возвращает настройки ClickHouse в виде словаря."""
        return {
            "host": self.CLICKHOUSE_HOST,
            "database": self.CLICKHOUSE_DB
        }

    def get_kafka_config(self):
        """Возвращает настройки Kafka в виде словаря."""
        return {
            "servers": self.KAFKA_SERVERS,
            "topic_request": self.KAFKA_TOPIC,
            "topic_response": self.KAFKA_TOPIC_RESPONSE
        }


# Создаем объект конфигурации
config = Config()

# Пример использования:
if __name__ == "__main__":
    print("ClickHouse Config:", config.get_clickhouse_config())
    print("Kafka Config:", config.get_kafka_config())
