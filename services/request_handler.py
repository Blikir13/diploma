import asyncio


class RequestHandler:
    def __init__(self, chain, kafka_producer):
        self.chain = chain
        self.kafka_producer = kafka_producer

    async def process_request(self, query, user_id):
        """Обрабатывает запрос и отправляет ответ в Kafka"""
        response = await self.chain.invoke(query)
        response_data = {"user_id": user_id, "response": response}

        # Отправляем ответ в Kafka
        self.kafka_producer.send_response(response_data)

        return response_data

    async def handle_multiple_requests(self, queries):
        """Обрабатывает несколько запросов одновременно"""
        tasks = [self.process_request(query['question'], query['user_id']) for query in queries]
        results = await asyncio.gather(*tasks)
        return results
