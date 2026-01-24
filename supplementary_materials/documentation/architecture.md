# Architecture Guide

## System Overview

The Ready Tensor RAG Assistant implements a three-tier architecture:

```
┌──────────────────┐
│  User Interface  │
│   (CLI/Web)      │
└────────┬─────────┘
         │
    Query Input
         │
         ▼
┌──────────────────┐
│  Query Processor │
│  (LangChain)     │
└────────┬─────────┘
         │
    Formatted Query
         │
         ▼
┌──────────────────┐     ┌──────────────────┐
│  Retriever       │────▶│  Vector Store    │
│  (Semantic)      │     │  (FAISS/Chroma)  │
└────────┬─────────┘     └──────────────────┘
         │
    Context Retrieved
         │
         ▼
┌──────────────────┐
│  LLM Chain       │     
│  (GPT/Claude)    │
└────────┬─────────┘
         │
    Generated Answer
         │
         ▼
┌──────────────────┐
│  Output Formatter│
│  & Display       │
└──────────────────┘
```

## Components

### Document Ingestion Pipeline
- Loads documents (PDF, TXT, MD)
- Splits documents into chunks
- Creates embeddings using OpenAI API
- Stores in vector database

### Retrieval System
- Semantic search using cosine similarity
- Returns top-k most relevant documents
- Ranks by relevance score

### LLM Integration
- Uses OpenAI GPT-3.5/GPT-4 API
- Receives context and query
- Generates contextual responses

### Response Generation
- Combines retrieved context with query
- Generates natural language answer
- Formats output for display

## Data Flow

1. **Input**: User asks question
2. **Embedding**: Question converted to vector
3. **Retrieval**: Similar documents found in vector store
4. **Context Building**: Top documents extracted
5. **Prompt Assembly**: Context + Question formatted
6. **LLM Call**: Prompt sent to language model
7. **Output**: Response generated and returned

## Performance Considerations

- Vector store is cached in memory for fast retrieval
- Batch processing for multiple queries
- Async operations for I/O
- Configurable chunk size and overlap
- Token limit management for LLM
