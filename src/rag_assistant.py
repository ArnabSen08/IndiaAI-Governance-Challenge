"""
RAG-Based AI Assistant - Main Pipeline
Demonstrates a working Retrieval-Augmented Generation system
"""

from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

class RAGAssistant:
    def __init__(self, api_key, vectorstore_path="./data/vectorstore"):
        """Initialize the RAG Assistant"""
        self.api_key = api_key
        self.vectorstore_path = vectorstore_path
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        self.llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7)
        
    def load_vectorstore(self):
        """Load existing vectorstore"""
        return FAISS.load_local(self.vectorstore_path, self.embeddings)
    
    def create_qa_chain(self):
        """Create the QA retrieval chain"""
        vectorstore = self.load_vectorstore()
        retriever = vectorstore.as_retriever()
        
        prompt_template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Answer:"""
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
        
        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt}
        )
        
        return qa
    
    def query(self, question: str) -> str:
        """Query the RAG assistant"""
        qa = self.create_qa_chain()
        answer = qa.run(question)
        return answer

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    assistant = RAGAssistant(api_key)
    
    # Example queries
    queries = [
        "What is the main objective of this project?",
        "What technologies are used in the RAG pipeline?",
    ]
    
    for query in queries:
        print(f"Q: {query}")
        answer = assistant.query(query)
        print(f"A: {answer}\n")
