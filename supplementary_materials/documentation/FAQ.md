# Frequently Asked Questions - Ready Tensor RAG

## General Questions

### Q1: What is RAG and why should I use it?
**A:** RAG (Retrieval-Augmented Generation) combines document retrieval with language models to answer questions based on your documents. You should use it when:
- You have domain-specific documents
- You need accurate, sourced answers
- You want to avoid AI hallucinations
- Your knowledge base changes frequently

### Q2: How is RAG different from fine-tuning?
**A:** 
| Aspect | RAG | Fine-tuning |
|--------|-----|-------------|
| **Speed** | Fast (minutes to hours) | Slow (days to weeks) |
| **Cost** | Low | High |
| **Updates** | Immediate | Requires retraining |
| **Data Size** | Works with any size | Needs lots of training data |
| **Transparency** | Source documents shown | Black box |

### Q3: Can I use RAG without OpenAI?
**A:** Yes! You can use:
- **Open Source LLMs:** Llama 2, Mistral, Falcon (via Ollama or local deployment)
- **Other Providers:** Anthropic Claude, Google PaLM, Cohere
- **Local Models:** Run everything on your machine with LM Studio

### Q4: What documents can RAG handle?
**A:** Currently supports:
- ✅ `.txt` - Plain text
- ✅ `.md` - Markdown
- ✅ `.pdf` - PDF files (with pdfplumber)
- ⚠️ `.docx` - Word documents (via python-docx)
- ⚠️ `.html` - Web pages (with BeautifulSoup)
- ⚠️ Images with text (OCR via Tesseract)

---

## Technical Questions

### Q5: How do I configure chunking parameters?
**A:**
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Characters per chunk
    chunk_overlap=200,    # Overlap between chunks
    separators=["\n\n", "\n", " ", ""]  # Split on these
)

# Tuning tips:
# - Larger chunks (1500+): Better context but slower retrieval
# - Smaller chunks (500-): Faster but may miss context
# - Overlap: Helps with split boundaries (10-20% of chunk size)
```

### Q6: How do I improve retrieval quality?
**A:** Use these strategies:
1. **Better Chunking:** Tune chunk size and overlap
2. **Preprocessing:** Clean documents, remove noise
3. **Metadata:** Add source, date, category info
4. **Hybrid Search:** Combine dense + sparse retrieval
5. **Query Expansion:** Rephrase queries multiple ways
6. **Re-ranking:** Use cross-encoder to rerank results

### Q7: What vector database should I use?
**A:**
| Database | Scale | Speed | Cost | Cloud |
|----------|-------|-------|------|-------|
| **FAISS** | 1M | Fast | Free | Local only |
| **Chroma** | 1M | Medium | Free | Self-hosted |
| **Pinecone** | 100M | Very Fast | Paid | ✅ Cloud |
| **Weaviate** | 100M | Fast | Free | ✅ Cloud |
| **Milvus** | 1B | Fast | Free | Self-hosted |

### Q8: How do I reduce costs?
**A:**
1. **Batch Process:** Process queries in batches (save 10-20%)
2. **Cache Responses:** Store answers to common questions (save 30-40%)
3. **Use Cheaper Models:** gpt-3.5-turbo vs gpt-4 (save 50%)
4. **Limit Context:** Retrieve fewer documents (save 5-10%)
5. **Embed Locally:** Use open-source embeddings (save embedding costs)

### Q9: How do I handle large documents?
**A:**
```python
# Strategy 1: Smaller chunks
chunk_size = 500  # Default is 1000

# Strategy 2: Hierarchical chunking
# Split into sections, then subsections

# Strategy 3: Summarization
# Summarize each chapter, then index

# Strategy 4: Sliding window
# Use overlapping windows over document

# Strategy 5: Multiple indices
# Separate index per document type
```

### Q10: Can I use RAG for real-time applications?
**A:** 
- **Latency:** ~1.2 seconds typical (LLM dependent)
- **Sub-second:** Possible with caching (for repeated queries)
- **Real-time Chat:** Yes, with streaming responses
- **Production:** Use CDN + edge caching for <200ms latency

---

## Troubleshooting

### Q11: My retrieval is returning irrelevant documents
**A:** Try these fixes:
1. Check document quality (typos, formatting)
2. Verify embeddings are working (`test_embeddings.py`)
3. Reduce chunk size to avoid mixing topics
4. Add more context/metadata
5. Try different embedding model
6. Check query is clear and complete

### Q12: Answers are still hallucinating
**A:**
1. Retrieve more documents (k=5 instead of k=3)
2. Use system prompt to enforce source attribution
3. Implement fact-checking against sources
4. Try different LLM (Claude often hallucinates less)
5. Fine-tune prompt templates

### Q13: Vector search is too slow
**A:**
1. Use GPU acceleration: `FAISS-GPU`
2. Reduce dimension: Use `text-embedding-3-small`
3. Pre-filter before search
4. Use approximate search (HNSW)
5. Add caching layer

### Q14: Out of memory errors
**A:**
```python
# Solution 1: Reduce vector store size
documents = documents[:10000]  # Limit docs

# Solution 2: Use sparse embeddings
# Reduces dimension significantly

# Solution 3: Use cloud vector DB
# Offload storage to cloud

# Solution 4: Increase batch size gradually
for batch in batches:
    vectorstore.add_documents(batch)
```

### Q15: API rate limiting issues
**A:**
```python
# Solution 1: Add retry logic
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def call_llm(prompt):
    return llm.call(prompt)

# Solution 2: Queue and batch
# Solution 3: Use caching
# Solution 4: Upgrade API plan
```

---

## Deployment Questions

### Q16: How do I deploy to production?
**A:** Three options:
1. **Docker:** `docker-compose up` (easiest)
2. **Cloud Platform:** AWS Lambda, Google Cloud Functions
3. **Kubernetes:** For high-scale deployments

See [DEPLOYMENT.md](./DEPLOYMENT.md) for details.

### Q17: Do I need a database?
**A:** 
- **Vector DB:** Yes (FAISS, Pinecone, Chroma)
- **Relational DB:** Optional (for metadata, logging)
- **Cache:** Recommended (Redis, in-memory)

### Q18: How do I monitor system performance?
**A:**
```python
# Track these metrics
metrics = {
    'latency': response_time,
    'tokens_used': tokens,
    'accuracy': human_eval,
    'cache_hit_rate': cache_hits / total,
    'error_rate': errors / total
}
```

### Q19: Can I run this locally without cloud APIs?
**A:** Yes! Use:
```python
# Ollama for local LLM
from langchain.llms import Ollama
llm = Ollama(model="llama2")

# Local embeddings
from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings()

# Local vector DB
from langchain.vectorstores import FAISS
```

### Q20: How do I handle sensitive data?
**A:**
1. Use local deployment (no cloud APIs)
2. Encrypt documents at rest
3. Use anonymization before retrieval
4. Implement access controls
5. Audit logging
6. Regular security reviews

---

## Advanced Topics

### Q21: How do I implement multi-language RAG?
**A:**
```python
# Use multilingual embeddings
from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/multilingual-MiniLM-L12-v2"
)

# Or use separate vector stores per language
```

### Q22: Can I use RAG with vision/images?
**A:** Yes, with:
- Multimodal embeddings (CLIP)
- OCR for text extraction
- Image search integration
- Vision LLMs (GPT-4V)

### Q23: How do I implement conversational RAG?
**A:**
```python
# Use memory to track conversation
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(return_messages=True)
chain = ConversationRetrievalChain.from_llm(
    llm, retriever, memory=memory
)
```

### Q24: How do I handle fact verification?
**A:**
```python
# Check facts against source documents
def verify_answer(answer, sources):
    # Extract claims from answer
    claims = extract_claims(answer)
    
    # Verify each claim in sources
    for claim in claims:
        if not claim_in_sources(claim, sources):
            return False, claim
    return True, None
```

### Q25: Can I use RAG with structured data?
**A:** Yes! Options:
1. Convert to text/documents
2. Use SQL retrieval
3. Graph databases
4. Combine with semantic search

---

## Performance & Optimization

### Q26: What's the maximum document collection size?
**A:**
- FAISS: 1M+ documents (billions with GPU)
- Production RAG: 10K-100K optimal
- Scaling strategy: Partition by domain/topic

### Q27: How often should I update documents?
**A:**
- **Frequently changing:** Update nightly
- **Stable data:** Update monthly
- **Real-time:** Use streaming updates
- **No rebuild:** Just append new chunks

### Q28: Can I get response streaming?
**A:** Yes!
```python
# Stream tokens as they arrive
for token in llm.stream(prompt):
    print(token, end='', flush=True)
```

### Q29: How do I debug retrieval problems?
**A:**
```python
# Debug retrieval
from langchain.callbacks import StdOutCallbackHandler

qa_chain = RetrievalQA.from_chain_type(
    llm, retriever,
    callbacks=[StdOutCallbackHandler()]
)
# Shows intermediate steps
```

### Q30: How do I measure answer quality?
**A:**
```python
# Manual evaluation metrics
- BLEU score (n-gram overlap)
- ROUGE score (recall-oriented)
- METEOR (synonym-aware)
- BERTScore (semantic)
- Human evaluation (gold standard)
```

---

## Getting Help

### Where to find answers?
1. **This FAQ** - Check here first
2. **Documentation:** `/docs` folder
3. **GitHub Issues:** Report bugs or ask questions
4. **Stack Overflow:** Tag with `langchain`, `rag`, `retrieval-augmented-generation`
5. **Discord/Forums:** LangChain community

### How to report issues?
1. Search existing issues
2. Provide reproducible example
3. Include Python version, OS, library versions
4. Describe expected vs actual behavior
5. Share error messages/logs

---

## Additional Resources

- **Official Docs:** https://python.langchain.com/
- **RAG Papers:** https://arxiv.org/search/?query=retrieval+augmented+generation
- **GitHub Repo:** https://github.com/ArnabSen08/ready-tensor
- **Community:** https://github.com/langchain-ai/langchain/discussions

---

**Last Updated:** January 2026  
**Maintained by:** Ready Tensor Project Team
