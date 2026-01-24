# Supplementary Materials - Ready Tensor RAG Project

This document indexes all supplementary materials that support the main publication.

## 📋 Index of Supplementary Materials

### 1. **Code & Implementation**
- [rag_assistant.py](../src/rag_assistant.py) - Main RAG pipeline implementation
- [demo.py](../demo.py) - Quick-start demo (no API keys required)
- [demo.ipynb](../notebooks/demo.ipynb) - Interactive Jupyter notebook

### 2. **Configuration & Setup**
- [.env.example](.env.example) - Environment variables template
- [requirements.txt](../requirements.txt) - Python dependencies
- [_config.yml](../_config.yml) - Jekyll/GitHub Pages configuration

### 3. **Documentation**
- [architecture.md](./architecture.md) - Detailed system architecture
- [examples.md](./examples.md) - Usage examples and patterns
- [setup.md](./setup.md) - Installation & configuration guide
- [BENCHMARKS.md](./BENCHMARKS.md) - Performance metrics and evaluation
- [FAQ.md](./FAQ.md) - Frequently asked questions
- [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Quick reference guide

### 4. **Data & Benchmarks**
- [sample_documents/](../data/documents/) - Sample documents for testing
- [benchmark_results.json](./benchmark_results.json) - Performance test results
- [evaluation_metrics.csv](./evaluation_metrics.csv) - Detailed evaluation data

### 5. **Deployment & DevOps**
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Production deployment guide
- [docker-compose.yml](../docker-compose.yml) - Docker containerization (optional)

### 6. **Media & Diagrams**
- [DIAGRAMS.md](./DIAGRAMS.md) - ASCII diagrams and visual explanations
- System architecture flowchart (in Methodology section)
- Data pipeline visualization

---

## 📖 How to Access Materials

### Via GitHub Repository
All materials are available at: https://github.com/ArnabSen08/ready-tensor

```
ready-tensor/
├── src/
│   ├── rag_assistant.py
│   ├── document_loader.py
│   └── retriever.py
├── docs/
│   ├── SUPPLEMENTARY_MATERIALS.md (this file)
│   ├── BENCHMARKS.md
│   ├── FAQ.md
│   ├── QUICK_REFERENCE.md
│   ├── DEPLOYMENT.md
│   ├── DIAGRAMS.md
│   ├── architecture.md
│   ├── examples.md
│   └── setup.md
├── data/
│   ├── documents/
│   └── benchmark_results.json
├── notebooks/
│   └── demo.ipynb
└── PUBLICATION.md
```

### Via GitHub Pages
Documentation site: https://arnabsen08.github.io/ready-tensor/

---

## 🚀 Quick Start with Supplementary Materials

### 1. **Learning Path**
Start with these materials in order:
1. [PUBLICATION.md](../PUBLICATION.md) - Main paper
2. [setup.md](./setup.md) - Installation
3. [demo.py](../demo.py) - Run quick demo
4. [QUICK_REFERENCE.md](./QUICK_REFERENCE.md) - Quick commands
5. [architecture.md](./architecture.md) - Deep dive into design

### 2. **Implementation Path**
For developers:
1. [setup.md](./setup.md) - Install dependencies
2. [src/rag_assistant.py](../src/rag_assistant.py) - Review main code
3. [notebooks/demo.ipynb](../notebooks/demo.ipynb) - Interactive tutorial
4. [examples.md](./examples.md) - Usage patterns

### 3. **Deployment Path**
For operations:
1. [DEPLOYMENT.md](./DEPLOYMENT.md) - Deployment strategies
2. [requirements.txt](../requirements.txt) - Dependencies
3. [docker-compose.yml](../docker-compose.yml) - Container setup
4. [BENCHMARKS.md](./BENCHMARKS.md) - Performance tuning

---

## 📊 Data Files

### Sample Documents
Located in: `data/documents/`

Sample document types:
- `.txt` - Plain text files
- `.pdf` - PDF documents (requires pdfplumber)
- `.md` - Markdown files

### Benchmark Results
Location: `docs/benchmark_results.json`

Contains:
- Query latencies
- Retrieval success rates
- Answer accuracy scores
- Token usage metrics

### Evaluation Metrics
Location: `docs/evaluation_metrics.csv`

Columns:
- query_id
- query_text
- retrieved_documents
- answer_generated
- accuracy_score
- latency_ms
- tokens_used

---

## 💻 Code Files

### Main Implementation
**File:** `src/rag_assistant.py`
- RAGAssistant class
- Vector store initialization
- QA chain creation
- Query processing
- Response formatting

### Document Loader
**File:** `src/document_loader.py` (template)
- Multi-format document loading
- Text chunking
- Embedding generation
- Vector store storage

### Demo Script
**File:** `demo.py`
- Quick demonstration
- No API keys required
- Shows system workflow
- Performance metrics

### Jupyter Notebook
**File:** `notebooks/demo.ipynb`
- Step-by-step walkthrough
- Interactive examples
- Visualizations
- Explanations

---

## 📚 Documentation Files

### Setup Guide
**File:** `docs/setup.md`
- Prerequisites
- Installation steps
- Environment configuration
- Troubleshooting

### Architecture
**File:** `docs/architecture.md`
- System design
- Component descriptions
- Data flow
- Performance considerations

### Examples
**File:** `docs/examples.md`
- Sample queries
- Use cases
- Integration examples
- Advanced patterns

### FAQ
**File:** `docs/FAQ.md`
- Common questions
- Troubleshooting
- Best practices
- Performance tips

### Quick Reference
**File:** `docs/QUICK_REFERENCE.md`
- Command cheat sheet
- Code snippets
- Configuration options
- API reference

### Benchmarks
**File:** `docs/BENCHMARKS.md`
- Performance metrics
- Comparison results
- Optimization techniques
- Scaling guidelines

---

## 🚢 Deployment Materials

### Deployment Guide
**File:** `docs/DEPLOYMENT.md`
- Local deployment
- Cloud deployment (AWS, GCP, Azure)
- Docker containerization
- Production considerations

### Docker Compose
**File:** `docker-compose.yml`
- Container orchestration
- Service configuration
- Volume management
- Network setup

---

## 🎨 Media & Diagrams

### System Architecture Diagram
ASCII representation in `docs/DIAGRAMS.md`

### Data Flow Diagram
Detailed flow chart in `docs/architecture.md`

### Performance Charts
Benchmark visualizations in `docs/BENCHMARKS.md`

---

## 📝 Configuration Templates

### Environment Variables
**File:** `.env.example`
```
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-3.5-turbo
```

### Python Requirements
**File:** `requirements.txt`
- langchain
- langchain-openai
- faiss-cpu
- openai
- python-dotenv

### Jekyll Configuration
**File:** `_config.yml`
- GitHub Pages settings
- Site metadata
- Build configuration

---

## 🔗 External Resources

### Official Documentation
- [LangChain Docs](https://python.langchain.com/)
- [OpenAI API](https://platform.openai.com/docs/)
- [FAISS Documentation](https://faiss.ai/)

### Related Papers
- Lewis et al. (2020) - RAG Paper
- Karpukhin et al. (2020) - Dense Passage Retrieval
- Devlin et al. (2019) - BERT

### Community Resources
- [LangChain GitHub](https://github.com/langchain-ai/langchain)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)
- [Ready Tensor Platform](https://ready-tensor.org/)

---

## 📦 How to Download Materials

### Option 1: Clone Repository
```bash
git clone https://github.com/ArnabSen08/ready-tensor.git
cd ready-tensor
```

### Option 2: Download Specific Files
From GitHub:
1. Navigate to the file
2. Click "Raw" button
3. Save to local machine

### Option 3: Download as ZIP
```bash
# Download entire repository as ZIP
curl -L https://github.com/ArnabSen08/ready-tensor/archive/refs/heads/master.zip
```

---

## ✅ Materials Checklist

- ✅ Main publication (PUBLICATION.md)
- ✅ Source code (src/)
- ✅ Demo script (demo.py)
- ✅ Jupyter notebook (notebooks/demo.ipynb)
- ✅ Setup documentation (docs/setup.md)
- ✅ Architecture guide (docs/architecture.md)
- ✅ Examples (docs/examples.md)
- ✅ FAQ (docs/FAQ.md)
- ✅ Quick reference (docs/QUICK_REFERENCE.md)
- ✅ Benchmarks (docs/BENCHMARKS.md)
- ✅ Deployment guide (docs/DEPLOYMENT.md)
- ✅ Configuration templates (.env.example, requirements.txt)
- ✅ Sample data (data/documents/)
- ✅ Benchmark results (docs/benchmark_results.json)
- ✅ Evaluation metrics (docs/evaluation_metrics.csv)

---

## 📧 Support & Questions

For questions about supplementary materials:
- Check [FAQ.md](./FAQ.md) first
- Review relevant documentation file
- Check GitHub Issues: https://github.com/ArnabSen08/ready-tensor/issues
- Visit GitHub Pages: https://arnabsen08.github.io/ready-tensor/

---

**Last Updated:** January 2026
**Version:** 1.0.0
**License:** Creative Commons Attribution-NonCommercial (CC BY-NC)
