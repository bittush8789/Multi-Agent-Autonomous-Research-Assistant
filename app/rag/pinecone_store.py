import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from app.models.settings import settings

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        if settings.PINECONE_API_KEY and settings.PINECONE_INDEX_NAME:
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Check if index exists, if not create it
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            if settings.PINECONE_INDEX_NAME not in existing_indexes:
                self.pc.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=384, # dimension for all-MiniLM-L6-v2
                    metric='cosine',
                    spec=ServerlessSpec(cloud='aws', region='us-east-1')
                )
            
            self.vector_db = PineconeVectorStore(
                index_name=settings.PINECONE_INDEX_NAME,
                embedding=self.embeddings,
                pinecone_api_key=settings.PINECONE_API_KEY
            )
        else:
            self.vector_db = None
            print("Warning: Pinecone not configured. PDF search will be disabled.")

    def process_pdf(self, file_path: str):
        if not self.vector_db:
            return 0
            
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = text_splitter.split_documents(documents)
        
        self.vector_db.add_documents(chunks)
        return len(chunks)

    def search(self, query: str, k: int = 3):
        if not self.vector_db:
            return []
        results = self.vector_db.similarity_search(query, k=k)
        return [res.page_content for res in results]

rag_service = RAGService()
