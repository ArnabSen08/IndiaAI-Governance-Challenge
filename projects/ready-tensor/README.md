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
✅ Professional demo videos (3 videos included)  

## Demo Videos

Watch our project in action:

### RAG System Demo (3 min)
Introductory demo showcasing key features and performance metrics.

<a href="https://github.com/ArnabSen08/ready-tensor/raw/master/supplementary_materials/videos/rag-demo.mp4" target="_blank">
  <img src="https://img.shields.io/badge/Watch%20Video-rag--demo-blue?style=for-the-badge&logo=youtube" alt="RAG Demo Video"/>
</a>

**Key Highlights:**
- System overview and capabilities
- 94% retrieval success rate
- 89% answer accuracy
- 1.2s average latency

---

### Architecture Walkthrough (5 min)
Technical deep-dive into the RAG system architecture and pipeline.

<a href="https://github.com/ArnabSen08/ready-tensor/raw/master/supplementary_materials/videos/architecture-walkthrough.mp4" target="_blank">
  <img src="https://img.shields.io/badge/Watch%20Video-architecture--walkthrough-green?style=for-the-badge&logo=youtube" alt="Architecture Video"/>
</a>

**Covers:**
- System components and data flow
- Query processing pipeline
- Embedding generation
- Vector search and retrieval
- LLM response generation

---

### Deployment Guide (4 min)
Step-by-step guide for deploying the RAG system to production.

<a href="https://github.com/ArnabSen08/ready-tensor/raw/master/supplementary_materials/videos/deployment-guide.mp4" target="_blank">
  <img src="https://img.shields.io/badge/Watch%20Video-deployment--guide-orange?style=for-the-badge&logo=youtube" alt="Deployment Video"/>
</a>

**Topics:**
- Local Docker deployment
- Cloud deployment options (AWS, Google Cloud, Azure)
- Configuration and setup
- Security best practices
- Production checklist

---

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
- [Supplementary Materials](./supplementary_materials/INDEX.md) - Benchmarks, FAQ, Quick Reference, and more
- [Performance Benchmarks](./supplementary_materials/BENCHMARKS.md)
- [Deployment Guide](./supplementary_materials/DEPLOYMENT.md)

## Video Resources

All demo videos are available in [supplementary_materials/videos/](./supplementary_materials/videos/):
- `rag-demo.mp4` - System overview and key metrics (693 KB)
- `architecture-walkthrough.mp4` - Technical architecture deep-dive (611 KB)
- `deployment-guide.mp4` - Production deployment tutorial (698 KB)

## License

Creative Commons Attribution-NonCommercial (CC BY-NC)

## Authors

- Ready Tensor Project Team

---

**Status**: Capstone Project | **Certification**: Agentic AI Essentials
