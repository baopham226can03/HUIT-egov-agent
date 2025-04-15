from src.common.vector_store import VectorStore
from src.common.pdf_processor import PDFProcessor
from src.chatbot import Chatbot
from src.common.config import Config

class SubBot:
    def __init__(self, name, data_path, collection_name):
        self.name = name
        self.data_path = data_path
        self.collection_name = collection_name
        self.vector_store = VectorStore(collection_name)
        self.processor = PDFProcessor(self.vector_store)
        self.chatbot = Chatbot(self.vector_store)
        self._initialize()

    def _initialize(self):
        self.processor.process_pdfs(self.data_path)

    def process_query(self, query):
        response, subbot_prompts = self.chatbot.handle_query(query)
        return response, subbot_prompts