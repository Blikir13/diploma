from chat_bot.database.db_connector import ClickHouseConnector
from chat_bot.models.chain import ResponseChain
from chat_bot.models.model import ResponseModel
from chat_bot.models.retriever import ContextRetriever
from services.kafka_consumer import KafkaRequestConsumer
from services.request_handler import RequestHandler
from services.kafka_producer import KafkaResponseProducer


def main():
    # Настройка Kafka Consumer для получения запросов
    producer = KafkaResponseProducer()

    clickhouse_connector = ClickHouseConnector()
    retriever = ContextRetriever()  # Предполагаем, что у вас есть этот класс
    model = ResponseModel()  # Предполагаем, что у вас есть этот класс

    # Создаем цепочку для ответа
    response_chain = ResponseChain(retriever, model, clickhouse_connector)

    request_handler = RequestHandler(response_chain, producer)
    consumer = KafkaRequestConsumer(request_handler)

    consumer.consume_requests()


if __name__ == "__main__":
    main()
