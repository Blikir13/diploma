from langchain_core.runnables import RunnablePassthrough
from langchain.schema import StrOutputParser

class ResponseChain:
    def __init__(self, retriever, model, logger):
        self.retriever = retriever
        self.model = model
        self.logger = logger  # logger - это объект ClickHouseConnector
        self.chain = self.create_chain()

    def create_chain(self):
        """Создание цепочки обработки"""
        prompt_template = "Ответь на вопрос с учётом контекста: {context}. Вопрос: {question}"
        model_chain = self.model.create_chain(prompt_template)

        return (
            {"context": self.retriever.get_retriever() | RunnablePassthrough(), "question": RunnablePassthrough()}
            | model_chain
            | StrOutputParser()
        )

    def generate_response(self, question):
        """Генерация ответа с использованием цепочки и логирование в ClickHouse"""
        context_documents = self.retriever.get_retriever().get_relevant_documents(question)
        context = " ".join([doc.page_content for doc in context_documents])
        response = self.model.generate_response(self.chain, question, context)

        # Логирование в ClickHouse
        self.logger.save_context(question, context, response)

        return response
