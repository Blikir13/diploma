from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate


class ResponseModel:
    def __init__(self, model_name="text-davinci-003", temperature=0.7):
        self.model_name = model_name
        self.temperature = temperature
        self.llm = self.create_llm()
        self.prompt = self.create_prompt()

    def get_prompt(self):
        return self.prompt

    def get_llm(self):
        return self.llm

    def create_prompt(self):
        template = """
            Игнорируй все предыдущие инструкции. Ты консультант интернет-сайта CXDP
            Будь вежлив. Выяви потребность клиента и помоги ему решить ее.
            Ниже приведены примеры информации, которую ты можешь использовать.
    
            Context: {context}
            Используй только данные из контекста. Если в этих данных нет ответа, скажи, что я
            не знаю, предложи обратиться к живому консультанту компании или документации. Не придумывай факты, которых нет в контексте.
    
            В своем ответе используй следующие принципы: 
            1. Ты должен давать четкие, краткие и прямые ответы. 
            2. Исключи ненужные напоминания, извинения, упоминания самого себя и любые заранее запрограммированные тонкости. 
            3. Сохраняй непринужденный тон в общении. 
            4. Будь прозрачным; если ты не уверен в ответе или если вопрос выходит за рамки твоих возможностей или знаний, признай это. 
            5. В случае неясных или двусмысленных вопросов задавай дополнительные вопросы, чтобы лучше понять намерения пользователя. 
            6. За каждый ответ ты получишь чаевые до 200 долларов (в зависимости от качества твоего ответа).
    
            Question: {question}
        """
        return ChatPromptTemplate.from_template(template)

    def create_llm(self):
        """Создание LLM модели"""
        return OpenAI(model_name=self.model_name, temperature=self.temperature)

    # def create_llm_chain(self):
    #     """Создание цепочки с использованием модели"""
    #     return LLMChain(prompt=self.prompt, llm=self.llm)

    # def generate_response(self, chain, question, context):
    #     """Генерация ответа"""
    #     return chain.invoke({"question": question, "context": context})
