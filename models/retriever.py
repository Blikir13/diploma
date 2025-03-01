from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

class ContextRetriever:
    def __init__(self, doc_path='doc.txt', model_name="cointegrated/LaBSE-en-ru"):
        self.doc_path = doc_path
        self.model_name = model_name
        self.retriever = None
        self._create_retriever()

    def _create_retriever(self):
        """Создание ретривера из документов"""
        # Чтение документа
        with open(self.doc_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Разбиение текста на части
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=10,
            length_function=len
        )
        texts = text_splitter.create_documents([content])

        # Генерация эмбеддингов
        hf_embeddings_model = HuggingFaceEmbeddings(model_name=self.model_name)

        # Создание FAISS базы данных
        db = FAISS.from_documents(texts, hf_embeddings_model)

        # Преобразование в ретривер
        self.retriever = db.as_retriever()

    def get_retriever(self):
        """Получение готового ретривера"""
        return self.retriever
