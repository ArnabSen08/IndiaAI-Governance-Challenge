# Ready Tensor - RAG-Based AI Assistant

A Retrieval-Augmented Generation (RAG) powered question-answering assistant built with LangChain, designed to retrieve answers from custom knowledge bases.

## Project Overview

This project is the capstone deliverable for the **Agentic AI Essentials Certification Program**. It demonstrates a working RAG pipeline that combines:

- **Prompt Formulation**: Crafting effective queries
- **Vector Store Retrieval**: Using FAISS/Chroma for semantic search
- **LLM Response Generation**: Generating contextual answers
- **Document Ingestion**: Building searchable knowledge bases

## Features

✅ LangChain-based RAG pipeline  
✅ Vector store integration (FAISS/Chroma)  
✅ Custom document knowledge base  
✅ Question-answering interface  
✅ Example queries and demonstrations  

## Getting Started

### Prerequisites

- Python 3.8+
- pip or conda
- GitHub account

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ready-tensor.git
cd ready-tensor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

```bash
python src/rag_assistant.py
```

## Project Structure

```
ready-tensor/
├── src/
│   ├── rag_assistant.py      # Main RAG pipeline
│   ├── document_loader.py    # Document ingestion
│   └── retriever.py          # Vector store retrieval
├── data/
│   └── documents/            # Knowledge base documents
├── notebooks/
│   └── demo.ipynb            # Demo notebook
├── requirements.txt
└── README.md
```

## Documentation

- [Architecture](./docs/architecture.md)
- [Setup Guide](./docs/setup.md)
- [Example Queries](./docs/examples.md)

## License

Creative Commons Attribution-NonCommercial (CC BY-NC)

## Authors

- Ready Tensor Project Team

---

**Status**: Capstone Project | **Certification**: Agentic AI Essentials
