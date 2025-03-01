import uuid

from clickhouse_driver import Client
from chat_bot.config.settings import config

class ClickHouseConnector:
    """Класс для подключения к ClickHouse и выполнения запросов."""

    def __init__(self):
        settings = config.get_clickhouse_config()
        self.client = Client(host=settings["host"], database=settings["database"])

    def save_context(self, question, context, response):
        """Сохранение запроса, контекста и ответа в ClickHouse"""
        query = "INSERT INTO chat_context (id, question, context, response) VALUES"
        data = [(str(uuid.uuid4()), question, context, response)]
        self.client.insert(query, data)

# Пример использования
if __name__ == "__main__":
    db = ClickHouseConnector()
    result = db.execute_query("SELECT 'Test connection to ClickHouse'")
    print(result)
