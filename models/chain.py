from langchain_core.runnables import RunnablePassthrough
from langchain.schema import StrOutputParser
from langchain.chains import LLMChain

from models.model import ResponseModel


class ResponseChain:
    def __init__(self, retriever, model:ResponseModel, logger):
        self.retriever = retriever
        self.model = model
        self.logger = logger  # logger - это объект ClickHouseConnector
        self.chain = self.create_chain()

    def create_llm_chain(self):
        """Создание цепочки с использованием модели"""
        return LLMChain(prompt=self.model.get_prompt(), llm=self.model.get_llm())

    def create_chain(self):
        """Создание цепочки обработки"""
        model_chain = self.create_llm_chain()

        return (
            {"context": self.retriever.get_retriever() | RunnablePassthrough(), "question": RunnablePassthrough()}
            | model_chain
            | StrOutputParser()
        )

    def generate_response(self, question):
        """Генерация ответа с использованием цепочки и логирование в ClickHouse"""
        context_documents = self.retriever.get_retriever().get_relevant_documents(question)
        context = " ".join([doc.page_content for doc in context_documents])
        response = self.chain.invoke({"question": question, "context": context})

        # Логирование в ClickHouse
        self.logger.save_context(question, context, response)

        return response
