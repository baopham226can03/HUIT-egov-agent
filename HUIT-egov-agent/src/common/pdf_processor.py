import PyPDF2
import os
from tqdm import tqdm
from openai import OpenAI
from src.common.config import Config
from src.common.vector_store import VectorStore

class PDFProcessor:
    def __init__(self, vector_store: VectorStore):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.vector_store = vector_store
        self.max_tokens = 2000

    def extract_text_from_pdf(self, pdf_path):
        text = ""
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text

    def split_text(self, text, max_tokens):
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            word_tokens = len(word) // 4 + 1
            if current_length + word_tokens > max_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = word_tokens
            else:
                current_chunk.append(word)
                current_length += word_tokens
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        return chunks

    def get_embedding(self, text):
        response = self.client.embeddings.create(
            model=Config.EMBEDDING_MODEL,
            input=text
        )
        return response.data[0].embedding

    def process_pdfs(self, directory):
        pdf_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(".pdf")]
        documents = []
        embeddings = []
        ids = []

        for pdf_path in tqdm(pdf_files, desc=f"Processing PDFs in {directory}"):
            text = self.extract_text_from_pdf(pdf_path)
            if text:
                chunks = self.split_text(text, self.max_tokens)
                for i, chunk in enumerate(chunks):
                    embedding = self.get_embedding(chunk)
                    doc_id = f"{os.path.basename(pdf_path)}_chunk_{i}"
                    documents.append(chunk)
                    embeddings.append(embedding)
                    ids.append(doc_id)

        if documents:
            self.vector_store.add_documents(documents, embeddings, ids)
            print(f"Processed and stored {len(documents)} chunks from {directory}.")