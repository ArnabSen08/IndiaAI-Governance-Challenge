import os
import faiss
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

class NFRAChatbot:
    """
    RAG-based chatbot for NFRA documents.
    """
    def __init__(self):
        # Initialize Embedding Model
        # Using a small model for speed in this environment
        try:
           self.model = SentenceTransformer('all-MiniLM-L6-v2') 
        except:
           # Fallback mostly for syntax checking if model download fails (though pip installed it)
           print("Warning: Failed to load SentenceTransformer. Chatbot will struggle.")
           self.model = None

        self.index = None
        self.documents = [] # List of dicts: {'content': str, 'metadata': dict}
        
        # Load Mock Knowledge Base on Init
        self._build_mock_knowledge_base()

    def _build_mock_knowledge_base(self):
        """
        Populate the vector store with simulated NFRA documents.
        """
        mock_docs = [
            {
                'content': "NFRA Audit Quality Review Report 2024: The Authority found that in 25% of cases, the Engagement Quality Control Reviewer (EQCR) failed to document the review process adequately.",
                'metadata': {'source': 'AQR Report 2024', 'page': 12, 'category': 'Audit Quality'}
            },
            {
                'content': "Circular on IndAS 115 Compliance: Revenue from contracts with customers must be recognized when performance obligations are satisfied. Entities must disclose the transaction price allocated to remaining performance obligations.",
                'metadata': {'source': 'Circular 2023-05', 'page': 2, 'category': 'IndAS Guidelines'}
            },
            {
                'content': "Whistleblower Protection: NFRA guarantees confidentiality for all whistleblowers reporting non-compliance with auditing standards. Reports can be submitted via the secure portal.",
                'metadata': {'source': 'Vigil Mechanism Policy', 'page': 5, 'category': 'Governance'}
            },
            {
                'content': "Auditor Rotation Guidelines: Statutory auditors must be rotated every 5 years for listed companies to ensure independence. Cooling off period is 5 years.",
                'metadata': {'source': 'Companies Act Sec 139', 'page': 45, 'category': 'Compliance'}
            }
        ]
        
        # Chunking simulation (splitting long text if we had it, here they are short)
        self.documents = mock_docs
        
        if self.model:
            embeddings = self.model.encode([d['content'] for d in self.documents])
            
            # Create FAISS Index
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings.astype('float32'))

    def query_knowledge_base(self, query: str, user_role: str = "Auditor") -> Dict:
        """
        Query the RAG system.
        """
        if not self.model or not self.index:
            return {'answer': "System initializing, please try again.", 'sources': []}
        
        # Log query (Mock)
        print(f"[AUDIT LOG] User: {user_role} | Query: {query}")
        
        # 1. Retrieve
        query_vector = self.model.encode([query])
        k = 2 # Top 2 results
        distances, indices = self.index.search(query_vector.astype('float32'), k)
        
        results = []
        context = ""
        
        for idx in indices[0]:
            if idx < len(self.documents):
                doc = self.documents[idx]
                results.append(doc)
                context += f"- {doc['content']}\n"
        
        # 2. Generate Answer (Simulated LLM)
        # In a real system, we would pass 'context' + 'query' to GPT/Llama.
        # Here we construct a credible answer from the retrieved chunks.
        
        answer = "Based on NFRA guidelines:\n\n"
        for doc in results:
            answer += f"• {doc['content']} (Source: {doc['metadata']['source']})\n"
            
        return {
            'answer': answer,
            'sources': results,
            'compliance_check': "Authorized"
        }
